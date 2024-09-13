python3 script.py

## Environnement:
python3 -m venv venv
source venv/bin/activate

## mot d p app

ybxn ivvs twwj smvi 

```python
# Liste des URLs des flux RSS
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
    # Ajoutez d'autres flux RSS ici
]
```

Prétraitement du texte :

    Utilisez spaCy pour le prétraitement, qui inclut la tokenisation, le lemmatisation, et la suppression des stop words.

```python
import spacy

# Charger le modèle spaCy
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)
    ```

Évaluation et Sélection des Articles

    Analyser et évaluer les articles :
        Utilisez des techniques de NLP pour analyser les articles. Par exemple, vous pouvez utiliser la fréquence des mots, l'analyse de sentiment, ou l'extraction de sujets pour évaluer l'importance des articles.
    Utiliser des modèles de classification ou de clustering :
        Vous pouvez entraîner un modèle de machine learning pour classer ou regrouper les articles selon leur pertinence. Par exemple, utilisez scikit-learn pour appliquer des algorithmes de clustering comme KMeans.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def evaluate_articles(articles):
    # Convertir les articles en vecteurs TF-IDF
    vector
```

---

Pour évaluer et sélectionner des articles en utilisant la fréquence des mots, l'analyse de sentiment, et l'extraction de sujets, vous pouvez suivre ces étapes en utilisant Python et des bibliothèques NLP :
1. Fréquence des mots
Utilisez NLTK ou spaCy pour analyser la fréquence des mots dans vos articles. Cela peut vous aider à identifier les termes les plus courants et potentiellement importants.

python
import spacy
from collections import Counter

# Charger le modèle français de spaCy
nlp = spacy.load("fr_core_news_sm")

def word_frequency(text):
    doc = nlp(text)
    words = [token.text for token in doc if token.is_alpha and not token.is_stop]
    return Counter(words).most_common(10)

# Exemple d'utilisation
text = "Votre texte d'article ici."
print(word_frequency(text))

2. Analyse de sentiment
Bien que spaCy ne propose pas directement d'analyse de sentiment, vous pouvez utiliser TextBlob pour cela. Notez que TextBlob est plus adapté pour l'anglais, mais il peut être utilisé pour le français avec des résultats limités.

python
from textblob import TextBlob

def sentiment_analysis(text):
    blob = TextBlob(text)
    return blob.sentiment

# Exemple d'utilisation
print(sentiment_analysis(text))

3. Extraction de sujets
Utilisez TopicRank, une méthode non supervisée basée sur des graphes pour extraire les termes-clés et les sujets principaux d'un document.

python
# TopicRank nécessite une implémentation spécifique ou l'utilisation de bibliothèques tierces.
# Voici une approche simplifiée en utilisant spaCy pour extraire des mots-clés.

def extract_keywords(text):
    doc = nlp(text)
    keywords = [chunk.text for chunk in doc.noun_chunks]
    return keywords

# Exemple d'utilisation
print(extract_keywords(text))

Évaluation et Sélection
Après avoir extrait ces informations, vous pouvez évaluer l'importance des articles en fonction de critères tels que la fréquence des mots-clés pertinents, le sentiment global (positif, négatif, neutre), et les sujets couverts. Vous pouvez créer un score composite pour chaque article et sélectionner ceux avec les scores les plus élevés pour un examen plus approfondi. En combinant ces techniques, vous pouvez automatiser l'évaluation et la sélection d'articles pertinents dans votre veille philosophique.

---

Améliorations Possibles
Pour mieux refléter l'originalité et l'intérêt philosophique, vous pourriez :

Ajouter un Score d'Originalité : Utiliser des techniques de similarité de texte pour comparer les articles et identifier ceux qui présentent des concepts ou des idées moins courants.
Utiliser des Indicateurs d'Écho : Intégrer des données externes, comme le nombre de partages sur les réseaux sociaux ou les citations dans d'autres articles, pour évaluer l'écho dans la communauté.

Génération de Rapports

    Création du Rapport HTML: Une fois les articles évalués, générez un rapport HTML résumant les articles sélectionnés.
    titre
    url
    date de publication
    résumé
    mots-clé qui pourront être utilisés sur le blog

    Envoi et Publication

    Envoi de la Newsletter: Utilisez un service comme Mailchimp ou un script Python avec SMTP pour envoyer le rapport par email. + si possible un rapport détaillé en markdown en pj qui reprédn toutes les évaluation des articles des 7 derniers jours (pas seulement des cinq sélectionnés)
    Publication sur un Blog: Si vous utilisez un CMS comme WordPress, vous pouvez automatiser la publication via des plugins ou des scripts utilisant l'API de WordPress. Ou github 

## modifications

Demander: 1 site par flux => 10 nouvelles ?
Ou : ajouter des sites, 8 nouvelles et demander max 1 par site

## Vérifier
- chaque site fonctionne: liste rss
- renouvellement sur une semaine
- tags cliquables dans un blog
- Envoi en html ou markdown sur site github jekyll
## Nouveaux sites

```python
`http://blog.ac-versailles.fr/oeildeminerve/index.php/feed/rss2`,
`http://la-philosophie.com/feed`,
`http://iphilo.fr/feed/`,
`https://journals.openedition.org/asterion/backend?format=rssdocuments&type=review`,
`https://journals.openedition.org/asterion/backend?format=rssdocuments`,
`http://blog.ac-versailles.fr/oeildeminerve/index.php/feed/rss2`,
`http://journals.openedition.org/leportique/backend?format=rssdocuments&type=review`,
```

En anglais, voir: https://www.similarweb.com/fr/top-websites/science-and-education/philosophy/ 

Divers
https://sites.unimi.it/chiasmi/

Deuxième problème : 
j'execute plusieurs fois le script pour test. J'ai ajouté des sites à consulter dans le script, mais les résultats du rapport sont toujours les mêmes: les cinq mêmes sites sélectionnés alors que j'ai ajouté des sources. Pourquoi ? J'ai l'impression que le script ne consulte pas les sites mais reprend les anciennes executions de script et sélections


Titre : ajouter à "Nouveautés en philosophie" la date de publication du rapport

Mettre un sous-titre: 

Voici une sélection d'articles philosophiques du mois écoulé.

Mettre en bas de page, après le résumé des articles :

Sources :  
[Actu Philosophia](https://www.actu-philosophia.com/), [Implications philosophiques](http://www.implications-philosophiques.org/), [La vie des idées](http://www.laviedesidees.fr/), [Non Fiction](https://www.nonfiction.fr/),  [Philitt](http://philitt.fr), [Radio France, Philosophie](https://www.radiofrance.fr/rss/sciences-savoirs/philosophie),[Philo-sciences](https://philosciences.com), [Anthropogoniques](https://anthropogoniques.com/),[Philosophia](http://philosophia.fr/),[Un Philosophe](http://unphilosophe.wordpress.com/), [L'Oeil de Minerve](http://blog.ac-versailles.fr/oeildeminerve/index.php/), [La philosophie](http://la-philosophie.com/), [iPhilo](http://iphilo.fr/), [Asterion](https://journals.openedition.org/asterion/), [Le Portique](http://journals.openedition.org/leportique/)


## Bash et raycast

Pour exécuter votre script Python à l'aide de Raycast avec un raccourci clavier, vous pouvez configurer un Script Command dans Raycast. Voici comment procéder :
Étapes pour Configurer un Script Command dans Raycast

    Créer un Script Bash pour Exécuter Votre Script Python :
        Créez un fichier bash qui active votre environnement virtuel et exécute votre script Python.

```bash
#!/bin/bash
source /path/to/your/virtualenv/bin/activate
python /path/to/your/script.py
deactivate
'''

Enregistrez ce fichier sous un nom comme run_script.sh et rendez-le exécutable :

```bash
chmod +x /path/to/run_script.sh
```

Créer un Script Command dans Raycast :

    Ouvrez Raycast et allez dans l'onglet Extensions.
    Cliquez sur "Create Script Command" et sélectionnez "New Script Command".

Configurer le Script Command :

    Remplissez les métadonnées requises pour le Script Command. Voici un exemple de configuration :

```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Run Weekly Script
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 📅
# @raycast.packageName Weekly Automation

/path/to/run_script.sh
```

    Assurez-vous que le chemin vers votre script bash est correct.
    Attribuer un Raccourci Clavier :
        Dans Raycast, allez dans les paramètres de l'application.
        Trouvez votre Script Command et attribuez-lui un raccourci clavier pour l'exécuter rapidement.

Points Importants

    Environnement Virtuel : Assurez-vous que votre script bash active correctement l'environnement virtuel avant d'exécuter le script Python.
    Permissions : Assurez-vous que votre script bash est exécutable.
    Raycast : Utilisez Raycast pour exécuter le script manuellement avec le raccourci clavier que vous avez configuré.

En suivant ces étapes, vous pouvez exécuter votre script Python à l'aide de Raycast avec un raccourci clavier, sans avoir besoin de planifier l'exécution.

## Projet

créer deux autres scipts: anglais et espagnol, et les poster sur le blog