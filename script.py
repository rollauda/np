# FONCTIONNE script consulter les articles des 30 derniers jours des feeds, CONVERTIT EN MARKDOWN AVEC YAML ET LIENS CLIQUABLES, et fichier texte used_articles

import feedparser
from newspaper import Article, Config
from datetime import datetime, timedelta
import spacy
from collections import Counter
from textblob import TextBlob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import html2text
from pathlib import Path
import html2text
import yaml
import os
from dotenv import load_dotenv
from github import Github
import sys

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Définir le chemin absolu vers votre projet
BASE_DIR = Path('/Users/rollandauda/Github/veille')
POSTS_DIR = os.path.join(BASE_DIR, '_posts')

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

def truncate_title(title, max_words=6):
    # Divisez le titre en mots
    words = title.split()
    # Tronquez le titre à max_words mots
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + '...'
    return title

def generate_html_report(articles, filename="rapport.html"):
    colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]  # Couleurs pastel
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    html_content = f"""
    <html>
    <head>
        <title>Veille philosophique</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .article {{ margin-bottom: 20px; padding: 10px; border-radius: 5px; }}
            h2 {{ color: #2E4053; }}
            p {{ margin: 5px 0; }}
            ul {{ list-style-type: disc; padding-left: 20px; }}
        </style>
    </head>
    <body>
        <h2>Actualités philosophiques</h2>
    """
    
    for index, article in enumerate(articles):
        color = colors[index % len(colors)]
        truncated_title = truncate_title(article['title'])  # Tronquer le titre à 6 mots
        keywords_links = ', '.join([f"[{kw[0]}]({kw[0]})" for kw in article['keywords'][:3]])
        html_content += f"""
        <div class="article" style="background-color: {color};">
            <h4>{truncated_title}</h4>
            <ul>
                <li><strong>Lien:</strong> <a href="{article['url']}">{article['url']}</a></li>
                <li><strong>Date de Publication:</strong> {article['publish_date']}</li>
                <li><strong>Résumé:</strong> {article['summary']}</li>
                <li><strong>Mots-clés:</strong> {keywords_links}</li>
            </ul>
        </div>
        """
    
    # Écrire le contenu HTML dans un fichier
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    return html_content

def generate_yaml_header(category):
    current_date = datetime.now().strftime("%Y-%m-%d")
    yaml_header = f"""---
layout: post
title: "Liens (fr)"
category: {category}
date: {current_date}
---
"""
    return yaml_header

def convert_html_to_markdown(html_content):
    h = html2text.HTML2Text()
    h.ignore_links = False  # Activer la conversion des liens HTML en Markdown
    h.ignore_images = True  # Ignorer les images dans le HTML

    # Convertir le HTML en Markdown
    markdown_content = h.handle(html_content)
    return markdown_content
    
    # Convertir les liens HTML en Markdown
    markdown_content = h.handle(html_content)

    # Remplacer les balises <a> par des liens Markdown
    markdown_content = markdown_content.replace('<a href="', '[')
    markdown_content = markdown_content.replace('</a>', '](')

    # Remplacer les balises <strong> par des mots-clés Markdown
    markdown_content = markdown_content.replace('<strong>', '**')
    markdown_content = markdown_content.replace('</strong>', '**')

    return markdown_content

def create_markdown_file(markdown_content, yaml_header, tags):
    current_date = datetime.now().strftime("%Y-%m-%d")
    file_name = f"{current_date}-nouveautes-en-philosophie.md"
    file_path = BASE_DIR / "_posts" / file_name

    # Ajouter les tags à l'en-tête YAML
    yaml_header += f"tags: {', '.join(tags)}\n"

    # Exemple d'utilisation : afficher le chemin pour vérification
    print(f"Le chemin complet du fichier est : {file_path}")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(yaml_header)
        file.write(markdown_content)

    return file_path

# Utilisation de la fonction
tags = ["philosophie"]
keywords = extract_keywords(article_text)  # Extraction des mots-clés
tags.extend(keywords)  # Ajout des mots-clés aux tags
markdown_file_path = create_markdown_file(markdown_content, yaml_header, tags)

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

# Convertir le HTML en Markdown
markdown_content = convert_html_to_markdown(html_content)

# Créer l'en-tête YAML
yaml_header = generate_yaml_header("philosophie française")

# Créer un nouveau fichier Markdown
markdown_file_path = create_markdown_file(markdown_content, yaml_header)

# Récupérer le token GitHub
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    raise ValueError("Le token GitHub n'est pas défini dans le fichier .env")

# Initialiser l'objet GitHub
g = Github(github_token)
try:
    repo = g.get_repo("rollauda/np")
    print("Accès au dépôt réussi.")
except github.GithubException as e:
    print(f"Erreur d'accès au dépôt : {e}")
# Récupérer le token GitHub
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    raise ValueError("Le token GitHub n'est pas défini dans le fichier .env")

# Initialiser l'objet GitHub
g = Github(github_token)
try:
    repo = g.get_repo("rollauda/np")
    print("Accès au dépôt réussi.")
except github.GithubException as e:
    print(f"Erreur d'accès au dépôt : {e}")

# Générer un nom de fichier avec la date actuelle
current_date = datetime.now().strftime("%Y-%m-%d")
file_name = f"{current_date}-nouveautes-en-philosophie.md"
file_path = os.path.join('_posts', file_name)

commit_message = 'Mise à jour automatique'

# Lire le contenu du fichier Markdown
with open(file_path, 'r') as file:
    content = file.read()

# Essayer de mettre à jour ou de créer le fichier sur GitHub
try:
    contents = repo.get_contents(file_path)
    repo.update_file(contents.path, commit_message, content, contents.sha)
except:
    repo.create_file(file_path, commit_message, content)

# Envoyer le rapport par e-mail
send_email(html_content, "veille philosophique", "rolland.auda@gmail.com")

# Mettre à jour le fichier avec les nouvelles URLs utilisées
write_used_urls([article['url'] for article in best_articles])

for article in best_articles:
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"Publish Date: {article['publish_date']}")
    print(f"Summary: {article['summary']}")
    print(f"Keywords: {article['keywords']}\n")
    print(f"Rapport envoyé par e-mail et enregistré en tant que {markdown_file_path}")
    print(f"Nouveau fichier de blog '{file_name}' téléversé sur le dépôt GitHub.")

