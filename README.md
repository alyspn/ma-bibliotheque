# ma-bibliotheque
projet devops + cda

# Application de Gestion de Bibliothèque

Ce projet est une simple application web de gestion de livres (style bibliothèque) développée avec Flask pour le backend et HTML/JavaScript pour le frontend. Le backend utilise une base de données SQLite pour stocker les informations sur les livres de manière persistante.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants sur votre système :

* **Python 3:** Assurez-vous que Python 3 (version 3.7 ou supérieure recommandée) est installé et accessible depuis votre terminal. Vous pouvez vérifier avec la commande `python --version` ou `python3 --version`.
* **pip:** Le gestionnaire de paquets pour Python. Il est généralement inclus avec les installations récentes de Python. Vous pouvez vérifier avec `pip --version` ou `pip3 --version`.
* **Git:** Nécessaire pour cloner le dépôt (si vous partez du code sur GitHub/GitLab).

## Installation

Suivez ces étapes pour configurer le projet sur votre machine locale :

1.  **Cloner le dépôt (si nécessaire) :**
    Si vous n'avez pas encore le code, clonez le dépôt depuis GitHub/GitLab :
    ```bash
    git clone <URL_DE_VOTRE_DEPOT>
    cd ma-bibliotheque
    ```
    Remplacez `<URL_DE_VOTRE_DEPOT>` par l'URL réelle de votre dépôt Git. Si vous avez déjà le code, naviguez simplement jusqu'au dossier racine du projet (`ma-bibliotheque`).

2.  **Naviguer vers le dossier backend :**
    Le backend contient les dépendances nécessaires.
    ```bash
    cd backend
    ```

4.  **Installer les dépendances Python :**
    Installez les bibliothèques requises listées dans `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Lancer l'Application

Une fois les dépendances installées :

1.  **Assurez-vous d'être dans le dossier `backend`** (et que votre environnement virtuel est activé si vous en utilisez un).

2.  **Lancez le serveur Flask :**
    ```bash
    python app.py
    ```
    Le terminal affichera des messages indiquant que le serveur démarre, notamment :
    ```
    * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
    ```
    Au premier lancement, il créera également le fichier de base de données `library.db` dans le dossier `backend`.

## Accéder à l'Application

1.  Ouvrez votre navigateur web préféré.
2.  Naviguez vers l'adresse suivante :
    [http://localhost:5000](http://localhost:5000) ou [http://127.0.0.1:5000](http://127.0.0.1:5000)

Vous devriez voir l'interface de l'application de bibliothèque, prête à être utilisée. Les livres que vous ajoutez seront sauvegardés dans la base de données SQLite.

## Arrêter l'Application

Pour arrêter le serveur Flask, retournez dans le terminal où il est en cours d'exécution et appuyez sur `Ctrl + C`.

Si vous utilisiez un environnement virtuel, vous pouvez le désactiver avec la commande :
```bash
deactivate
Structure du Projet/ma-bibliotheque
├── backend/
│   ├── app.py           # Code principal du serveur Flask et de l'API
│   ├── requirements.txt # Dépendances Python
│   └── library.db       # Fichier de base de données SQLite (créé au premier lancement)
│   └── venv/            # (Optionnel) Dossier de l'environnement virtuel
├── frontend/
│   └── index.html       # Fichier HTML de l'interface utilisateur
└── README.md            # Ce fichier
