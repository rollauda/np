#!/bin/bash

# Chemin vers le fichier de log
LOG_FILE="/Users/rollandauda/Github/veille/script.log"

# Enregistrer le début de l'exécution
echo "Script started at $(date)" >> $LOG_FILE

# Activer l'environnement virtuel
source /Users/rollandauda/Github/veille/venv/bin/activate

# Exécuter le script Python et capturer les erreurs
{
    python3 /Users/rollandauda/Github/veille/script.py
} || {
    # Enregistrer l'erreur si le script Python échoue
    echo "Script failed at $(date)" >> $LOG_FILE
}

# Désactiver l'environnement virtuel
deactivate

# Enregistrer la fin de l'exécution
echo "Script ended at $(date)" >> $LOG_FILE

