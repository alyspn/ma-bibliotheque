# Application de Gestion de Bibliothèque - Projet DevOps

## Introduction

Ce projet présente une application web simple de gestion de livres, développée dans le cadre d'une démonstration des principes et outils DevOps. L'application permet d'afficher une liste de livres et d'en ajouter de nouveaux. Elle est composée d'un backend en Python (Flask), d'un frontend en HTML/JavaScript, et utilise une base de données PostgreSQL (lorsqu'elle est lancée avec Docker ou Kubernetes).

L'objectif principal de ce dépôt est de démontrer un flux de travail DevOps complet, incluant la conteneurisation, l'intégration continue, le déploiement continu (jusqu'au registre d'images), et le déploiement sur Kubernetes.

## Architecture Générale

L'application est décomposée en plusieurs services :

1.  **Frontend :** Une interface utilisateur simple (HTML, CSS, JS).
2.  **Backend :** Une API RESTful développée avec **Flask** (Python).
3.  **Base de Données :** **PostgreSQL** (utilisée avec Docker/Kubernetes) ou **SQLite** (pour le lancement sans Docker).
4.  **Serveur Web Frontend (avec Docker/K8s) :** **Nginx** sert les fichiers statiques du frontend.
5.  **CI/CD :** Pipeline **GitHub Actions** pour linter, scanner, construire et pousser les images Docker vers **GHCR**, et simuler le déploiement K8s.
6.  **Orchestration (Local) :** **Docker Compose** pour l'environnement de développement local multi-conteneurs.
7.  **Orchestration (Déploiement) :** **Kubernetes** pour le déploiement (testé sur Docker Desktop).

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments nécessaires selon la méthode de lancement choisie :

* **Pour toutes les méthodes :**
    * **Git :** Pour cloner le dépôt.
* **Pour le lancement sans Docker :**
    * **Python 3:** Version 3.7+ recommandée.
    * **pip:** Gestionnaire de paquets Python.
* **Pour le lancement avec Docker Compose :**
    * **Docker Desktop :** Installé et en cours d'exécution.
* **Pour le déploiement sur Kubernetes :**
    * **Docker Desktop :** Installé, en cours d'exécution, et **Kubernetes activé** (Settings -> Kubernetes -> Enable Kubernetes).
    * **kubectl :** Outil en ligne de commande Kubernetes (généralement inclus et configuré par Docker Desktop).
    * **Compte GitHub et PAT :** Pour créer le secret d'accès à GHCR (voir section Kubernetes).

---

## Méthodes de Lancement

Vous pouvez lancer ce projet de trois manières différentes :

### Méthode 1 : Lancement Sans Docker (Développement Initial / Test Simple)

Cette méthode utilise directement Python sur votre machine et la base de données SQLite. Elle ne nécessite pas Docker mais ne représente pas l'environnement cible final.

1.  **Cloner le dépôt :**
    ```bash
    git clone <URL_DE_VOTRE_DEPOT>
    cd ma-bibliotheque
    ```
2.  **Naviguer vers le dossier backend :**
    ```bash
    cd backend
    ```
3.  **(Optionnel mais recommandé) Créer et activer un environnement virtuel :**
    ```bash
    # Créer
    python -m venv venv
    # Activer (Windows)
    .\venv\Scripts\activate
    # Activer (macOS/Linux)
    # source venv/bin/activate
    ```
4.  **Installer les dépendances Python :**
    * *Note :* Installe aussi `psycopg2-binary`, même s'il n'est pas utilisé dans cette configuration, car il est dans `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
5.  **Lancer le serveur Backend Flask :**
    * Le backend utilisera automatiquement le fichier `library.db` (SQLite) s'il ne trouve pas les variables d'environnement PostgreSQL.
    ```bash
    python app.py
    ```
    * Le serveur démarre sur `http://localhost:5000`. Laissez ce terminal ouvert.
6.  **Ouvrir le Frontend :**
    * Naviguez jusqu'au dossier `frontend` dans votre explorateur de fichiers.
    * Double-cliquez sur le fichier `index.html` pour l'ouvrir dans votre navigateur web.
    * L'interface devrait s'afficher et pouvoir communiquer avec le backend sur `http://localhost:5000`.
7.  **Arrêter :**
    * Arrêtez le serveur Flask en appuyant sur `Ctrl + C` dans son terminal.
    * Désactivez l'environnement virtuel (si utilisé) avec `deactivate`.

### Méthode 2 : Lancement avec Docker Compose (Environnement de Développement Local Complet)

Cette méthode utilise Docker pour créer un environnement isolé et reproductible avec tous les services (Frontend Nginx, Backend Flask, BDD PostgreSQL). C'est la méthode recommandée pour le développement.

1.  **Cloner le dépôt (si pas déjà fait) :**
    ```bash
    git clone <URL_DE_VOTRE_DEPOT>
    cd ma-bibliotheque
    ```
2.  **Assurez-vous que Docker Desktop est lancé.**
3.  **Construire les images (si nécessaire) :**
    La première fois, ou si vous modifiez les Dockerfiles.
    ```bash
    docker-compose build
    ```
4.  **Lancer tous les services :**
    ```bash
    docker-compose up -d
    ```
    * `-d` lance les conteneurs en arrière-plan.
5.  **Accéder à l'application :**
    * Ouvrez votre navigateur et allez sur `http://localhost:8080`. Le frontend (servi par Nginx) s'affiche et communique avec le backend (sur le port 5000, via le réseau Docker).
6.  **Vérifier les logs (si besoin) :**
    ```bash
    docker-compose logs -f # Affiche les logs de tous les services
    docker-compose logs -f backend # Logs spécifiques du backend
    ```
7.  **Arrêter les services :**
    ```bash
    docker-compose down
    ```
    * Cela arrête et supprime les conteneurs. Le volume `postgres_data` persiste.

### Méthode 3 : Déploiement sur Kubernetes (Simulation avec Docker Desktop)

Cette méthode déploie l'application sur un cluster Kubernetes local géré par Docker Desktop, en utilisant les images Docker stockées sur GHCR.

1.  **Cloner le dépôt (si pas déjà fait) et naviguer à la racine.**
2.  **Vérifier l'activation de Kubernetes dans Docker Desktop** et que `kubectl` est configuré (`kubectl config current-context` doit afficher `docker-desktop`).
3.  **Créer le Secret pour l'accès à GHCR (une seule fois) :**
    * Générez un [PAT GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) avec la permission `read:packages`.
    * Exécutez dans un terminal **PowerShell** (adaptez pour bash/zsh) :
        ```powershell
        kubectl create secret docker-registry ghcr-secret `
          --docker-server=ghcr.io `
          --docker-username=<VOTRE_USERNAME_GITHUB> `
          --docker-password=<VOTRE_PAT_GITHUB> `
          --docker-email=<VOTRE_EMAIL_GITHUB>
        ```
4.  **Appliquer les Manifestes Kubernetes :**
    ```bash
    kubectl apply -f kubernetes/
    ```
5.  **Vérifier le déploiement :**
    ```bash
    kubectl get pods -w
    ```
    * Attendez que tous les pods (`backend`, `frontend`, `postgres`) soient `Running` et `READY 1/1`. (`Ctrl+C` pour arrêter).
6.  **Trouver le NodePort du Frontend :**
    ```bash
    kubectl get service frontend-service
    ```
    * Notez le port élevé (ex: `3XXXX`) dans la colonne `PORT(S)` pour la ligne `80:XXXXX/TCP`.
7.  **Accéder à l'application :**
    * Ouvrez votre navigateur et allez sur `http://localhost:<NODE_PORT>`.
8.  **Nettoyer les ressources Kubernetes :**
    ```bash
    kubectl delete -f kubernetes/
    # Optionnel: kubectl delete secret ghcr-secret
    # Optionnel: kubectl delete pvc postgres-pvc
    ```

---

## Workflow de Développement et Stratégie de Branches

Ce projet adopte un workflow de développement simple mais efficace, inspiré de Git Flow, pour faciliter la gestion du code et la collaboration (même simulée).

**Stratégie de Branches :**

* **`main` :** Cette branche représente la version stable et "déployable" de l'application. Tout commit sur cette branche est considéré comme prêt pour la production (ou une simulation de production). Le pipeline CI/CD complet (incluant le push des images vers GHCR et la tentative de déploiement K8s) se déclenche sur les push vers `main`.
* **`dev` (ou autres branches de fonctionnalité) :** Le développement de nouvelles fonctionnalités ou la correction de bugs se fait sur des branches séparées (comme `dev` dans notre cas, ou des branches spécifiques comme `feature/ajout-livre`).
* **Pull Requests (PR) :** Avant d'intégrer les changements de `dev` (ou d'une autre branche) dans `main`, une Pull Request est créée sur GitHub. Cela permet :
    * Une revue de code (simulée ici).
    * Le déclenchement automatique du pipeline CI (sans le push des images ni le déploiement K8s) pour vérifier que les changements n'introduisent pas d'erreurs ou de régressions.
* **Merge :** Une fois la PR validée (revue et CI réussie), elle est mergée dans `main`. Ce merge déclenche un événement `push` sur `main`, lançant ainsi le pipeline CI/CD complet.

**Flux typique :**

1.  Créer une branche `dev` depuis `main`.
2.  Effectuer des modifications sur la branche `dev`.
3.  Pousser la branche `dev` sur GitHub.
4.  Créer une Pull Request de `dev` vers `main`.
5.  Le pipeline CI s'exécute sur la PR (tests, scans, build sans push).
6.  Si la CI réussit, merger la PR dans `main`.
7.  Le pipeline CI/CD complet s'exécute sur `main` (tests, scans, build, push vers GHCR, déploiement simulé K8s).

## Pipeline CI/CD Détaillé (GitHub Actions)

Le fichier `.github/workflows/ci.yml` définit le pipeline d'intégration et de déploiement continu.

**Déclencheurs :**
* Sur `push` vers la branche `main`.
* Sur `pull_request` ciblant la branche `main`.
* Manuellement (`workflow_dispatch`).

**Description des Jobs et Étapes Principales :**

* **Job 1 : `build-test-scan-push`** (S'exécute sur `push` et `pull_request` vers `main`)
    1.  **Checkout Code :** Récupère le code source.
    2.  **Setup Python :** Configure l'environnement Python.
    3.  **Install Dependencies :** Installe les dépendances Python du backend.
    4.  **Lint :** Analyse statique du code Python backend avec `Flake8`.
    5.  **Setup Docker Buildx :** Prépare l'outil de build Docker.
    6.  **Login to GHCR :** S'authentifie auprès de GitHub Container Registry.
    7.  **Extract Metadata :** Génère les tags et labels pour les images Docker.
    8.  **Build and Load Images :** Construit les images Docker backend et frontend.
    9.  **Push Images (Conditionnel) :** Pousse les images vers GHCR **uniquement si** l'événement est un `push` sur la branche `main`.
    10. **Scan Images :** Utilise `Trivy` pour scanner les images à la recherche de vulnérabilités.

* **Job 2 : `deploy-k8s`** (S'exécute **uniquement** après succès du Job 1 ET sur `push` vers `main`)
    1.  **Checkout Code :** Récupère le code source pour accéder aux manifestes.
    2.  **(Simulé) Apply Manifests :** Exécute `kubectl apply -f kubernetes/`. Cette étape démontre comment le déploiement serait automatisé mais échoue car le cluster local n'est pas accessible depuis GitHub Actions.

**Vérification :**
* Les résultats des exécutions sont visibles dans l'onglet "Actions" du dépôt GitHub.
* Les images poussées (après un push réussi sur `main`) sont visibles dans la section "Packages" du dépôt GitHub.

## Structure du Projet

/ma-bibliotheque├── .github/│   └── workflows/│       └── ci.yml             # Workflow GitHub Actions CI/CD├── backend/│   ├── app.py               # Application Flask (API)│   ├── Dockerfile           # Instructions pour construire l'image backend│   ├── requirements.txt     # Dépendances Python│   └── .dockerignore        # Fichiers à ignorer par Docker lors du build backend├── frontend/│   ├── index.html           # Interface utilisateur HTML/JS│   ├── Dockerfile           # Instructions pour construire l'image frontend (Nginx)│   └── .dockerignore        # Fichiers à ignorer par Docker lors du build frontend├── kubernetes/│   ├── backend-deployment.yaml  # Déploiement K8s pour le backend│   ├── backend-service.yaml     # Service K8s pour le backend│   ├── frontend-deployment.yaml # Déploiement K8s pour le frontend│   ├── frontend-service.yaml    # Service K8s pour le frontend│   ├── postgres-deployment.yaml # Déploiement K8s pour Postgres│   ├── postgres-secret.yaml     # Secret K8s pour les identifiants Postgres (généré manuellement)│   ├── postgres-service.yaml    # Service K8s pour Postgres│   └── postgres-storage.yaml    # PersistentVolumeClaim K8s pour Postgres├── .dockerignore            # Fichiers à ignorer par Docker (racine, si nécessaire)├── docker-compose.yml       # Configuration pour lancer l'app localement avec Docker Compose└── README.md                # Ce fichier de documentation
## Réponse aux Objectifs du Projet Final

Ce projet répond aux exigences du guide comme suit :

1.  **Culture DevOps :** Démontrée par l'utilisation de Git/GitHub/Branches/PR, la documentation (`README.md` incluant workflow et stratégie de branche), l'automatisation (CI/CD), et la standardisation des environnements (Docker).
2.  **Conteneurisation :** Réalisée avec des `Dockerfile` optimisés (base légère, cache), gestion des secrets/env via K8s Secrets et variables d'environnement, persistance des données BDD (Volumes/PVC), et utilisation d'un registre (GHCR). Les healthchecks sont implémentés via les Probes K8s.
3.  **Intégration Continue (CI) :** Mise en place avec GitHub Actions, incluant linting (Flake8), build des images, et scan de sécurité des images (Trivy). Déclenchée sur push/PR.
4.  **Déploiement Continu (CD) :** Structurellement en place avec un job dédié dans GitHub Actions qui pousse les images vers GHCR. Le déploiement final sur K8s est simulé (étape `kubectl apply` présente mais échoue car cible locale). La stratégie Rolling Update est utilisée implicitement par K8s.
5.  **Fonctionnement Local (Docker Compose) :** Assuré par `docker-compose.yml` qui orchestre backend, frontend et BDD avec persistance et réseau configurés.
6.  **Fonctionnement Kubernetes :** Démontré par le déploiement réussi sur le cluster local de Docker Desktop en utilisant les manifestes YAML fournis, incluant gestion des secrets (BDD, GHCR), persistance (PVC), et probes. L'accès se fait via NodePort.
7.  **Infrastructure as Code :** Non abordé (optionnel).

## Améliorations Possibles

* Ajouter des **tests unitaires et d'intégration** au backend et les exécuter dans la CI.
* Ajouter un **scan de sécurité du code source** (ex: `bandit`) dans la CI.
* Implémenter une ressource **Ingress** dans Kubernetes pour un accès externe plus propre (nécessite un Ingress Controller dans le cluster).
* Définir les **requests et limits de ressources** (CPU/mémoire) dans les manifestes Kubernetes.
* Configurer des **notifications** (Slack, email) pour les échecs de la CI/CD.
* Mettre en place un **déploiement CD fonctionnel vers un cluster distant** (cloud ou autre) en configurant l'authentification `kubectl` dans le workflow GitHub Actions.
* Implémenter des **stratégies de déploiement plus avancées** (Blue/Green, Canary) si nécessaire.
* Automatiser les **rollbacks** dans le pipeline CD en cas d'échec post-déploiement.
* Utiliser des **tags d'image Docker plus spécifiques** (ex: SHA du commit) dans Kubernetes au lieu de `:latest` ou `:main` pour un meilleur contrôle des versions déployées.
* Gérer les **secrets Kubernetes** de manière plus sécurisée (ex: via Vault ou des solutions cloud natives).
