# script consulter les articles des 30 derniers jours des feeds, et fichier texte used_articles

import feedparser
from newspaper import Article, Config
from datetime import datetime, timedelta
import spacy
from collections import Counter
from textblob import TextBlob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    html_content = f"""
    <html>
    <head>
        <title>Nouveautés en philosophie - {current_date}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .article {{ margin-bottom: 20px; padding: 10px; border-radius: 5px; }}
            h2 {{ color: #2E4053; }}
            p {{ margin: 5px 0; }}
            ul {{ list-style-type: disc; padding-left: 20px; }}
        </style>
    </head>
    <body>
        <h1>Nouveautés en philosophie - {current_date}</h1>
        <h2>Voici une sélection d'articles philosophiques du mois écoulé.</h2>
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
        <footer>
            <h3>Sources :</h3>
            <p>
                <a href='https://www.actu-philosophia.com/'>Actu Philosophia</a>, 
                <a href='http://www.implications-philosophiques.org/'>Implications philosophiques</a>, 
                <a href='http://www.laviedesidees.fr/'>La vie des idées</a>, 
                <a href='https://www.nonfiction.fr/'>Non Fiction</a>, 
                <a href='http://philitt.fr'>Philitt</a>, 
                <a href='https://www.radiofrance.fr/rss/sciences-savoirs/philosophie'>Radio France, Philosophie</a>,
                <a href='https://philosciences.com'>Philo-sciences</a>, 
                <a href='https://anthropogoniques.com/'>Anthropogoniques</a>,
                <a href='http://philosophia.fr/'>Philosophia</a>,
                <a href='http://unphilosophe.wordpress.com/'>Un Philosophe</a>, 
                <a href='http://blog.ac-versailles.fr/oeildeminerve/index.php/'>L'Oeil de Minerve</a>, 
                <a href='http://la-philosophie.com/'>La philosophie</a>, 
                <a href='http://iphilo.fr/'>iPhilo</a>, 
                <a href='https://journals.openedition.org/asterion/'>Asterion</a>, 
                <a href='http://journals.openedition.org/leportique/'>Le Portique</a>
            </p>
        </footer>
    </body>
    </html>
    """
    
    # Écrire le contenu HTML dans un fichier
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    return html_content

def send_email(html_content, subject, to_email):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "rolland.auda@gmail.com"  # Remplacez par votre e-mail
    app_password = "ybxn ivvs twwj smvi"  # Remplacez par votre mot de passe d'application

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email

    message.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, message.as_string())
            print("E-mail envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail: {e}")

def read_used_urls(filename="used_articles.txt"):
    try:
        with open(filename, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def write_used_urls(urls, filename="used_articles.txt"):
    with open(filename, "a") as file:
        for url in urls:
            file.write(url + "\n")

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
    'http://blog.ac-versailles.fr/oeildeminerve/index.php/feed/rss2',
    'http://la-philosophie.com/feed',
    'http://iphilo.fr/feed/',
    'https://journals.openedition.org/asterion/backend?format=rssdocuments&type=review',
    'https://journals.openedition.org/asterion/backend?format=rssdocuments',
    'http://journals.openedition.org/leportique/backend?format=rssdocuments&type=review',
]

def extract_best_article(feed_url, used_urls):
    print(f"Fetching articles from: {feed_url}")
    feed = feedparser.parse(feed_url, request_headers={'Cache-Control': 'no-cache'})
    articles = []
    now = datetime.now()
    one_month_ago = now - timedelta(days=30)

    for entry in feed.entries:
        article_url = entry.link
        if article_url in used_urls:
            continue  # Skip articles already used in the previous report

        published_date = datetime(*entry.published_parsed[:6]) if 'published_parsed' in entry else None
        if published_date and published_date < one_month_ago:
            continue  # Skip articles older than one month

        config = Config()
        config.memoize_articles = False  # Désactiver la mise en cache des articles
        article = Article(article_url, config=config)
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
                'publish_date': entry.published if 'published' in entry else 'N/A',
                'summary': summary,
                'sentiment': sentiment,
                'keywords': keywords
            })
        except Exception as e:
            print(f"Erreur lors du traitement de l'article {article_url}: {e}")
    
    # Sélectionner le meilleur article en fonction du sentiment et du nombre de mots-clés
    if articles:
        best_article = max(articles, key=lambda x: (x['sentiment'], len(x['keywords'])))
        return best_article
    return None

used_urls = read_used_urls()
best_articles = []
for feed_url in rss_feeds:
    best_article = extract_best_article(feed_url, used_urls)
    if best_article:
        best_articles.append(best_article)
        used_urls.add(best_article['url'])

# Générer le rapport HTML
html_content = generate_html_report(best_articles)

# Envoyer le rapport par e-mail
send_email(html_content, "Nouveautés en philosophie", "rolland.auda@gmail.com")

# Mettre à jour le fichier avec les nouvelles URLs utilisées
write_used_urls([article['url'] for article in best_articles])

for article in best_articles:
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"Publish Date: {article['publish_date']}")
    print(f"Summary: {article['summary']}")
    print(f"Keywords: {article['keywords']}\n")

