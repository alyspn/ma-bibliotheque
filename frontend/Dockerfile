# frontend/Dockerfile

# Étape 1: Base Image
# Utiliser une image Nginx officielle légère basée sur Alpine Linux.
FROM nginx:stable-alpine

# Étape 2: Copier les Fichiers du Frontend
# Copier le contenu du dossier frontend local (où se trouve ce Dockerfile)
# dans le répertoire par défaut où Nginx sert les fichiers HTML.
# Le '.' signifie le contenu du dossier courant (contexte de build).
# '/usr/share/nginx/html' est le dossier racine web par défaut de Nginx.
COPY . /usr/share/nginx/html

# Étape 3: Exposer le Port
# Indiquer à Docker que Nginx écoute sur le port 80 (port HTTP par défaut).
EXPOSE 80

# Étape 4: Commande de Lancement (implicite)
# L'image Nginx de base est configurée pour démarrer Nginx automatiquement.
# Aucune commande CMD n'est nécessaire ici, Nginx démarrera en avant-plan.

