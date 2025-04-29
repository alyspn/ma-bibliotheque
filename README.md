# Application de Gestion de Bibliothèque - Projet DevOps

## Introduction

Ce projet présente une application web simple de gestion de livres, développée dans le cadre d'une démonstration des principes et outils DevOps. L'application permet d'afficher une liste de livres et d'en ajouter de nouveaux. Elle est composée d'un backend en Python (Flask), d'un frontend en HTML/JavaScript, et utilise une base de données PostgreSQL.

L'objectif principal de ce dépôt est de démontrer un flux de travail DevOps complet, incluant la conteneurisation, l'intégration continue, le déploiement continu (jusqu'au registre d'images), et le déploiement sur Kubernetes.

## Architecture Générale

L'application est décomposée en plusieurs services conteneurisés :

1.  **Frontend :** Une interface utilisateur simple (HTML, CSS, JS) servie par un serveur web **Nginx**. Elle communique avec l'API backend.
2.  **Backend :** Une API RESTful développée avec **Flask** (Python). Elle gère la logique métier et interagit avec la base de données.
3.  **Base de Données :** Une base de données **PostgreSQL** pour stocker les informations des livres de manière persistante.
4.  **CI/CD :** Un pipeline **GitHub Actions** est configuré pour automatiser les tests (linting), les scans de sécurité (Trivy), la construction des images Docker, et le push des images vers **GitHub Container Registry (GHCR)**. Il inclut également une étape de déploiement simulée vers Kubernetes.
5.  **Orchestration (Local) :** **Docker Compose** est utilisé pour lancer et gérer l'ensemble des services (frontend, backend, BDD) en environnement de développement local.
6.  **Orchestration (Déploiement) :** **Kubernetes** est utilisé pour déployer l'application. Les manifestes YAML décrivent l'état désiré des services dans le cluster. Le déploiement a été testé sur le cluster Kubernetes fourni par **Docker Desktop**.

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

**Visualisation Simplifiée du Flux :**

```mermaid
graph LR
    A[Commit sur dev] --> B(Push dev vers GitHub);
    B --> C{Création Pull Request vers main};
    C --> D[Job CI: build-test-scan-push<br>(sur PR)];
    D -- ✅ Succès --> E{Merge PR dans main};
    E --> F[Push vers main];
    F --> G[Job CI: build-test-scan-push<br>(sur main)];
    G -- ✅ Succès --> H[Job CD: deploy-k8s<br>(sur main)];
    D -- ❌ Échec --> I[Correction sur dev];
    I --> B;
    G -- ❌ Échec --> J[Analyse Échec CI];
    H -- (Simulé) --> K[Déploiement K8s];

    style D fill:#eee,stroke:#333,stroke-width:2px;
    style G fill:#eee,stroke:#333,stroke-width:2px;
    style H fill:#eee,stroke:#333,stroke-width:2px;
    style K fill:#f9f,stroke:#333,stroke-width:2px;


(Note: Ce diagramme utilise la syntaxe Mermaid et s'affichera correctement sur GitHub et les plateformes compatibles.)
Description des Jobs et Étapes Principales :
Job 1 : build-test-scan-push (S'exécute sur push et pull_request vers main)
Checkout Code : Récupère le code source.
Setup Python : Configure l'environnement Python.
Install Dependencies : Installe les dépendances Python du backend.
Lint : Analyse statique du code Python backend avec Flake8.
Setup Docker Buildx : Prépare l'outil de build Docker.
Login to GHCR : S'authentifie auprès de GitHub Container Registry.
Extract Metadata : Génère les tags et labels pour les images Docker.
Build and Load Images : Construit les images Docker backend et frontend.
Push Images (Conditionnel) : Pousse les images vers GHCR uniquement si l'événement est un push sur la branche main.
Scan Images : Utilise Trivy pour scanner les images à la recherche de vulnérabilités.
Job 2 : deploy-k8s (S'exécute uniquement après succès du Job 1 ET sur push vers main)
Checkout Code : Récupère le code source pour accéder aux manifestes.
(Simulé) Apply Manifests : Exécute kubectl apply -f kubernetes/. Cette étape démontre comment le déploiement serait automatisé mais échoue car le cluster local n'est pas accessible depuis GitHub Actions.
Vérification :
Les résultats des exécutions sont visibles dans l'onglet "Actions" du dépôt GitHub.
Les images poussées (après un push réussi sur main) sont visibles dans la section "Packages" du dépôt GitHub.
Prérequis
Avant de commencer, assurez-vous d'avoir installé :
Git : Pour cloner le dépôt.
Docker Desktop : Assurez-vous que Docker Desktop est installé, en cours d'exécution, et que Kubernetes est activé dans ses paramètres (Settings -> Kubernetes -> Enable Kubernetes).
kubectl : L'outil en ligne de commande pour interagir avec Kubernetes. Il est généralement inclus et configuré par Docker Desktop lorsque Kubernetes est activé. Vérifiez avec kubectl config current-context (devrait afficher docker-desktop).
Compte GitHub et PAT (pour Kubernetes) : Un compte GitHub est nécessaire pour GHCR. Pour déployer sur Kubernetes, un Personal Access Token (PAT) avec la permission read:packages est requis pour créer le secret d'accès à GHCR.
Lancement en Développement Local (Docker Compose)
Cette méthode est idéale pour le développement et les tests rapides.
Cloner le dépôt :
git clone <URL_DE_VOTRE_DEPOT>
cd ma-bibliotheque


Construire les images (si nécessaire) :
La première fois, ou si vous modifiez les Dockerfiles.
docker-compose build


Lancer les services :
docker-compose up -d


-d lance les conteneurs en arrière-plan.
Accéder à l'application :
Ouvrez votre navigateur et allez sur http://localhost:8080.
Arrêter les services :
docker-compose down


Cela arrête et supprime les conteneurs. Le volume de la base de données (postgres_data) persiste.
Déploiement sur Kubernetes (via Docker Desktop)
Cette section décrit le déploiement manuel sur le cluster Kubernetes local fourni par Docker Desktop.
Vérifier l'activation de Kubernetes : Assurez-vous que Kubernetes est activé dans Docker Desktop et que kubectl config current-context retourne docker-desktop.
Créer le Secret pour GHCR (si pas déjà fait) :
Générez un Personal Access Token (PAT) sur GitHub avec la permission read:packages.
Ouvrez un terminal PowerShell (ou adaptez pour bash/zsh) à la racine du projet.
Exécutez (remplacez les placeholders) :
kubectl create secret docker-registry ghcr-secret `
  --docker-server=ghcr.io `
  --docker-username=<VOTRE_USERNAME_GITHUB> `
  --docker-password=<VOTRE_PAT_GITHUB> `
  --docker-email=<VOTRE_EMAIL_GITHUB>


Appliquer les Manifestes Kubernetes :
Depuis la racine du projet :
kubectl apply -f kubernetes/


Cela crée toutes les ressources : Deployments, Services, Secret (pour Postgres), PVC. Les Deployments utilisent le ghcr-secret pour tirer les images privées.
Vérifier le déploiement :
kubectl get pods -w


Attendez que tous les pods (backend, frontend, postgres) soient Running et READY.
Trouver le NodePort du Frontend :
kubectl get service frontend-service


Notez le port élevé (ex: 3XXXX) dans la colonne PORT(S) pour la ligne 80:XXXXX/TCP.
Accéder à l'application :
Ouvrez votre navigateur et allez sur http://localhost:<NODE_PORT>.
Nettoyer les ressources Kubernetes :
kubectl delete -f kubernetes/
# Optionnel: supprimer le secret GHCR
# kubectl delete secret ghcr-secret
# Optionnel: supprimer le PVC (attention, supprime les données BDD)
# kubectl delete pvc postgres-pvc


Structure du Projet
/ma-bibliotheque
├── .github/
│   └── workflows/
│       └── ci.yml             # Workflow GitHub Actions CI/CD
├── backend/
│   ├── app.py               # Application Flask (API)
│   ├── Dockerfile           # Instructions pour construire l'image backend
│   ├── requirements.txt     # Dépendances Python
│   └── .dockerignore        # Fichiers à ignorer par Docker lors du build backend
├── frontend/
│   ├── index.html           # Interface utilisateur HTML/JS
│   ├── Dockerfile           # Instructions pour construire l'image frontend (Nginx)
│   └── .dockerignore        # Fichiers à ignorer par Docker lors du build frontend
├── kubernetes/
│   ├── backend-deployment.yaml  # Déploiement K8s pour le backend
│   ├── backend-service.yaml     # Service K8s pour le backend
│   ├── frontend-deployment.yaml # Déploiement K8s pour le frontend
│   ├── frontend-service.yaml    # Service K8s pour le frontend
│   ├── postgres-deployment.yaml # Déploiement K8s pour Postgres
│   ├── postgres-secret.yaml     # Secret K8s pour les identifiants Postgres (généré manuellement)
│   ├── postgres-service.yaml    # Service K8s pour Postgres
│   └── postgres-storage.yaml    # PersistentVolumeClaim K8s pour Postgres
├── .dockerignore            # Fichiers à ignorer par Docker (racine, si nécessaire)
├── docker-compose.yml       # Configuration pour lancer l'app localement avec Docker Compose
└── README.md                # Ce fichier de documentation


Réponse aux Objectifs du Projet Final
Ce projet répond aux exigences du guide comme suit :
Culture DevOps : Démontrée par l'utilisation de Git/GitHub/Branches/PR, la documentation (README.md incluant workflow et stratégie de branche), l'automatisation (CI/CD), et la standardisation des environnements (Docker).
Conteneurisation : Réalisée avec des Dockerfile optimisés (base légère, cache), gestion des secrets/env via K8s Secrets et variables d'environnement, persistance des données BDD (Volumes/PVC), et utilisation d'un registre (GHCR). Les healthchecks sont implémentés via les Probes K8s.
Intégration Continue (CI) : Mise en place avec GitHub Actions, incluant linting (Flake8), build des images, et scan de sécurité des images (Trivy). Déclenchée sur push/PR.
Déploiement Continu (CD) : Structurellement en place avec un job dédié dans GitHub Actions qui pousse les images vers GHCR. Le déploiement final sur K8s est simulé (étape kubectl apply présente mais échoue car cible locale). La stratégie Rolling Update est utilisée implicitement par K8s.
Fonctionnement Local (Docker Compose) : Assuré par docker-compose.yml qui orchestre backend, frontend et BDD avec persistance et réseau configurés.
Fonctionnement Kubernetes : Démontré par le déploiement réussi sur le cluster local de Docker Desktop en utilisant les manifestes YAML fournis, incluant gestion des secrets (BDD, GHCR), persistance (PVC), et probes. L'accès se fait via NodePort.
Infrastructure as Code : Non abordé (optionnel).
Améliorations Possibles
Ajouter des tests unitaires et d'intégration au backend et les exécuter dans la CI.
Ajouter un scan de sécurité du code source (ex: bandit) dans la CI.
Implémenter une ressource Ingress dans Kubernetes pour un accès externe plus propre (nécessite un Ingress Controller dans le cluster).
Définir les requests et limits de ressources (CPU/mémoire) dans les manifestes Kubernetes.
Configurer des notifications (Slack, email) pour les échecs de la CI/CD.
Mettre en place un déploiement CD fonctionnel vers un cluster distant (cloud ou autre) en configurant l'authentification kubectl dans le workflow GitHub Actions.
Implémenter des stratégies de déploiement plus avancées (Blue/Green, Canary) si nécessaire.
Automatiser les rollbacks dans le pipeline CD en cas d'échec post-déploiement.
Utiliser des tags d'image Docker plus spécifiques (ex: SHA du commit) dans Kubernetes au lieu de :latest ou :main pour un meilleur contrôle des versions déployées.
Gérer les secrets Kubernetes de manière plus sécurisée (ex: via
