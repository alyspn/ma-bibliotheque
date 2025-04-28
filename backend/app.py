# backend/app.py
# --- Imports ---
import os
import time # Importé pour une éventuelle attente de la BDD
from flask import Flask, jsonify, request, send_from_directory # Vérifier qu'il n'y a pas d'espace avant 'from'
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError # Pour attraper les erreurs de connexion DB

# --- Configuration ---
# Détermine le chemin absolu du dossier où se trouve ce script
basedir = os.path.abspath(os.path.dirname(__file__)) # Pas d'indentation ici

# Initialise l'application Flask
app = Flask(__name__, static_folder='../frontend', static_url_path='/') # Pas d'indentation
CORS(app, resources={r"/api/*": {"origins": "*"}}) # Pas d'indentation

# --- Configuration de la Base de Données PostgreSQL ---
# Lire les informations de connexion depuis les variables d'environnement
DB_USER = os.environ.get('POSTGRES_USER', 'user_fallback') # Pas d'indentation
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password_fallback') # Pas d'indentation
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost') # Pas d'indentation
DB_PORT = os.environ.get('POSTGRES_PORT', '5432') # Pas d'indentation
DB_NAME = os.environ.get('POSTGRES_DB', 'db_fallback') # Pas d'indentation

# Construire l'URI de la base de données
DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" # Pas d'indentation
print(f"Tentative de connexion à la base de données : postgresql://{DB_USER}:******@{DB_HOST}:{DB_PORT}/{DB_NAME}") # Pas d'indentation

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI # Pas d'indentation
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Pas d'indentation

# Initialise l'extension SQLAlchemy
db = SQLAlchemy(app) # Pas d'indentation
# --- Fin de la Configuration DB ---

# --- Modèle de Base de Données ---
# Définit la structure de la table 'book'
class Book(db.Model): # Pas d'indentation pour la définition de classe
    # Indentation correcte pour les attributs de la classe (généralement 4 espaces)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    # Indentation correcte pour les méthodes de la classe
    def to_dict(self):
        # Indentation correcte pour le corps de la méthode
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author
        }
# --- Fin du Modèle DB ---

# --- Initialisation de la Base de Données ---
# Fonction pour essayer de créer les tables, avec tentatives en cas d'échec initial
def initialize_database(app_context): # Pas d'indentation pour la définition de fonction
    with app_context: # Indentation correcte pour le bloc 'with'
        max_retries = 5
        retries = 0
        while retries < max_retries: # Indentation correcte pour la boucle 'while'
            try: # Indentation correcte pour le bloc 'try'
                print("Vérification et création des tables de la base de données si nécessaire...")
                db.create_all()
                print("Tables vérifiées/créées avec succès.")
                return # Sortir si succès
            except OperationalError as e: # Indentation correcte pour le bloc 'except'
                retries += 1
                print(f"Erreur de connexion à la BDD: {e}")
                print(f"Nouvelle tentative dans 5 secondes... ({retries}/{max_retries})")
                time.sleep(5) # Attendre 5 secondes avant de réessayer
        # Ce code est au même niveau d'indentation que la boucle 'while'
        print("ERREUR: Impossible de se connecter à la base de données après plusieurs tentatives.")
        # Optionnel: sortir du script si la BDD n'est pas accessible
        # import sys
        # sys.exit(1)

# Appel de l'initialisation dans le contexte de l'application
initialize_database(app.app_context()) # Pas d'indentation
# --- Fin Initialisation DB ---


# --- Définition des Routes ---

# Route pour servir le fichier index.html du frontend
@app.route('/') # Pas d'indentation pour le décorateur
def serve_index(): # Pas d'indentation pour la définition de fonction
    """Sert le fichier index.html du dossier frontend."""
    # Indentation correcte pour le corps de la fonction
    print("Requête reçue pour servir index.html")
    if not app.static_folder or not os.path.isdir(app.static_folder):
         print(f"ERREUR: Le dossier static_folder '{app.static_folder}' n'est pas configuré ou n'existe pas.")
         return "Erreur de configuration serveur.", 500
    index_path = os.path.join(app.static_folder, 'index.html')
    if not os.path.isfile(index_path):
         print(f"ERREUR: Le fichier 'index.html' n'a pas été trouvé dans {app.static_folder}")
         return "Fichier index.html non trouvé.", 404
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"Erreur inattendue lors de la tentative de servir index.html: {e}")
        return "Erreur serveur interne.", 500


# --- Routes API Modifiées (pour inclure la gestion d'erreur DB) ---

@app.route('/api/books', methods=['GET']) # Pas d'indentation
def get_books(): # Pas d'indentation
    """Retourne la liste de tous les livres depuis la base de données."""
    # Indentation correcte
    print("Requête GET reçue pour /api/books")
    try:
        all_books = Book.query.all()
        result = [book.to_dict() for book in all_books]
        return jsonify(result)
    except OperationalError as e:
         print(f"Erreur BDD lors de la récupération des livres: {e}")
         return jsonify({"error": "Erreur de connexion à la base de données"}), 503 # Service Unavailable
    except Exception as e:
        print(f"Erreur serveur lors de la récupération des livres: {e}")
        return jsonify({"error": "Erreur serveur interne"}), 500


@app.route('/api/books', methods=['POST']) # Pas d'indentation
def add_book(): # Pas d'indentation
    """Ajoute un nouveau livre à la base de données."""
    # Indentation correcte
    print("Requête POST reçue pour /api/books")
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        return jsonify({"error": "Les champs 'title' et 'author' sont requis."}), 400

    try:
        new_book = Book(title=request.json['title'], author=request.json['author'])
        db.session.add(new_book)
        db.session.commit()
        print(f"Livre ajouté à la BDD : {new_book.to_dict()}")
        return jsonify(new_book.to_dict()), 201
    except OperationalError as e:
         print(f"Erreur BDD lors de l'ajout du livre: {e}")
         db.session.rollback()
         return jsonify({"error": "Erreur de connexion à la base de données lors de l'ajout"}), 503
    except Exception as e:
        print(f"Erreur serveur lors de l'ajout du livre: {e}")
        db.session.rollback()
        return jsonify({"error": "Erreur serveur interne lors de l'ajout"}), 500

# --- Démarrage du Serveur ---
# Ce bloc s'exécute seulement si le script est lancé directement
if __name__ == '__main__': # Pas d'indentation
    # Indentation correcte pour le corps du 'if'
    if app.static_folder:
        abs_static_folder = os.path.abspath(app.static_folder)
        print(f"Vérification de l'existence du dossier frontend (static_folder) à: {abs_static_folder}")
        if not os.path.isdir(abs_static_folder):
             print(f"ERREUR: Le dossier frontend n'a pas été trouvé à {abs_static_folder}")
             print("Assurez-vous que les dossiers 'backend' et 'frontend' sont au même niveau.")
        else:
             print("Dossier frontend trouvé.")
    else:
        print("ERREUR: static_folder n'est pas configuré pour l'application Flask.")

    print("Démarrage du serveur Flask sur http://localhost:5000 (accessible via 0.0.0.0 dans le conteneur)")
    app.run(debug=True, host='0.0.0.0', port=5000)

