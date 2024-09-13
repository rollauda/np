import feedparser
from newspaper import Article
from datetime import datetime, timedelta
import spacy
from collections import Counter
from textblob import TextBlob

# Charger le modèle français de spaCy
nlp = spacy.load('fr_core_news_sm')

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def extract_keywords(text, top_n=10):
    doc = nlp(text)
    words = [token.text for token in doc if not token.is_stop and token.is_alpha]
    return Counter(words).most_common(top_n)

def generate_summary(text, sentence_count=3):
    sentences = text.split('. ')
    return '. '.join(sentences[:sentence_count]) + '.'

def generate_html_report(articles, filename="rapport.html"):
    colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]  # Couleurs pastel
    
    html_content = """
    <html>
    <head>
        <title>Rapport de Veille Philosophique</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .article { margin-bottom: 20px; padding: 10px; border-radius: 5px; }
            h2 { color: #2E4053; }
            p { margin: 5px 0; }
            ul { list-style-type: disc; padding-left: 20px; }
        </style>
    </head>
    <body>
        <h1>Nouveautés en philosophie</h1>
    """
    
    for index, article in enumerate(articles):
        color = colors[index % len(colors)]
        keywords_links = ', '.join([f"<a href='#{kw[0]}'>{kw[0]}</a>" for kw in article['keywords'][:3]])
        html_content += f"""
        <div class="article" style="background-color: {color};">
            <h2>{article['title']}</h2>
            <ul>
                <li><strong>Lien:</strong> <a href="{article['url']}">{article['url']}</a></li>
                <li><strong>Date de Publication:</strong> {article['publish_date']}</li>
                <li><strong>Résumé:</strong> {article['summary']}</li>
                <li><strong>Mots-clés:</strong> {keywords_links}</li>
            </ul>
        </div>
        """
    
    html_content += """
    </body>
    </html>
    """
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)

rss_feeds = [
    'https://www.actu-philosophia.com/feed/',
    'http://www.implications-philosophiques.org/feed/',
    'http://www.laviedesidees.fr/spip.php?page=backend',
    'https://www.nonfiction.fr/rss-critiques.xml',
    'http://philitt.fr/feed/',
    'https://www.radiofrance.fr/rss/sciences-savoirs/philosophie',
    'https://philosciences.com/?format=feed&type=rss',
    'https://anthropogoniques.com/feed/',
    'http://philosophia.fr/feed/',
    'http://unphilosophe.wordpress.com/feed/',
]

def extract_recent_articles(feed_url, days=7):
    feed = feedparser.parse(feed_url)
    articles = []
    now = datetime.now()
    cutoff_date = now - timedelta(days=7)

    for entry in feed.entries:
        published_date = datetime(*entry.published_parsed[:6]) if 'published_parsed' in entry else None
        if published_date and published_date >= cutoff_date:
            article_url = entry.link
            article = Article(article_url)
            try:
                article.download()
                article.parse()
                processed_text = preprocess_text(article.text)
                sentiment = analyze_sentiment(article.text)
                keywords = extract_keywords(processed_text)
                summary = generate_summary(article.text)
                articles.append({
                    'title': article.title,
                    'url': article_url,
                    'publish_date': published_date.strftime('%Y-%m-%d'),
                    'summary': summary,
                    'sentiment': sentiment,
                    'keywords': keywords
                })
            except Exception as e:
                print(f"Erreur lors du traitement de l'article {article_url}: {e}")
    
    return articles

all_articles = []
for feed_url in rss_feeds:
    recent_articles = extract_recent_articles(feed_url)
    all_articles.extend(recent_articles)

all_articles.sort(key=lambda x: (x['sentiment'], len(x['keywords'])), reverse=True)

top_articles = all_articles[:5]

generate_html_report(top_articles)

for article in top_articles:
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"Publish Date: {article['publish_date']}")
    print(f"Summary: {article['summary']}")
    print(f"Keywords: {article['keywords']}\n")
