# backend/Dockerfile

# Étape 1: Base Image
# Utiliser une image Python officielle légère comme point de départ.
# 'python:3.9-slim' est une bonne option (taille réduite). Adapte la version si besoin.
FROM python:3.9-slim

# Définir des variables d'environnement (bonnes pratiques)
# Simplification pour éviter les erreurs de parsing potentielles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Étape 2: Définir le Répertoire de Travail
# Crée et définit le répertoire où le code de l'application vivra dans le conteneur.
WORKDIR /app

# Étape 3: Copier et Installer les Dépendances
# Copier uniquement le fichier requirements.txt d'abord pour profiter du cache Docker.
# Si requirements.txt ne change pas, Docker n'aura pas besoin de réinstaller les dépendances.
COPY requirements.txt .

# Installer les dépendances Python listées dans requirements.txt.
# --no-cache-dir réduit la taille de l'image en n'enregistrant pas le cache pip.
# --upgrade pip s'assure que pip est à jour.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Étape 4: Copier le Code de l'Application
# Copier le reste du code du backend (app.py, etc.)
# dans le répertoire de travail /app du conteneur.
# Assurez-vous que .dockerignore est configuré pour exclure les fichiers non nécessaires (venv, .git, library.db etc.)
COPY . .

# Étape 5: Exposer le Port
# Indiquer à Docker que l'application écoute sur le port 5000 à l'intérieur du conteneur.
EXPOSE 5000

# Étape 6: Commande de Lancement
# La commande à exécuter lorsque le conteneur démarre.
# 'host=0.0.0.0' est essentiel pour que l'application soit accessible depuis l'extérieur du conteneur.
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Alternative avec Gunicorn (si ajouté à requirements.txt):
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

