# backend/app.py
# --- Imports ---
import os
import time
from flask import Flask, jsonify, request # send_from_directory n'est plus nécessaire
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

# --- Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialise l'application Flask SANS configuration static_folder
app = Flask(__name__)
# Appliquer CORS à toutes les routes (plus simple maintenant que le frontend est séparé)
CORS(app)

# --- Configuration de la Base de Données PostgreSQL (inchangée) ---
DB_USER = os.environ.get('POSTGRES_USER', 'user_fallback')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password_fallback')
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PORT = os.environ.get('POSTGRES_PORT', '5432')
DB_NAME = os.environ.get('POSTGRES_DB', 'db_fallback')

DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"Tentative de connexion à la base de données : postgresql://{DB_USER}:******@{DB_HOST}:{DB_PORT}/{DB_NAME}")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# --- Fin de la Configuration DB ---

# --- Modèle de Base de Données (inchangé) ---
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author
        }
# --- Fin du Modèle DB ---

# --- Initialisation de la Base de Données (inchangée) ---
def initialize_database(app_context):
    with app_context:
        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                print("Vérification et création des tables de la base de données si nécessaire...")
                db.create_all()
                print("Tables vérifiées/créées avec succès.")
                return
            except OperationalError as e:
                retries += 1
                print(f"Erreur de connexion à la BDD: {e}")
                print(f"Nouvelle tentative dans 5 secondes... ({retries}/{max_retries})")
                time.sleep(5)
        print("ERREUR: Impossible de se connecter à la base de données après plusieurs tentatives.")

initialize_database(app.app_context())
# --- Fin Initialisation DB ---


# --- Définition des Routes API UNIQUEMENT ---

# Route racine simple pour vérifier que l'API fonctionne
@app.route('/')
def home():
     """Route simple pour vérifier que le serveur API est en cours d'exécution."""
     # Retourne juste un message simple ou un statut, pas une page HTML.
     return jsonify({"status": "API Backend de la Bibliothèque en cours d'exécution"})


@app.route('/api/books', methods=['GET'])
def get_books():
    print("Requête GET reçue pour /api/books")
    try:
        all_books = Book.query.all()
        result = [book.to_dict() for book in all_books]
        return jsonify(result)
    except OperationalError as e:
         print(f"Erreur BDD lors de la récupération des livres: {e}")
         return jsonify({"error": "Erreur de connexion à la base de données"}), 503
    except Exception as e:
        print(f"Erreur serveur lors de la récupération des livres: {e}")
        return jsonify({"error": "Erreur serveur interne"}), 500


@app.route('/api/books', methods=['POST'])
def add_book():
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
if __name__ == '__main__':
    print("Démarrage du serveur API Flask sur http://localhost:5000 (accessible via 0.0.0.0 dans le conteneur)")
    # host='0.0.0.0' est essentiel pour l'accès depuis d'autres conteneurs/hôte
    app.run(debug=True, host='0.0.0.0', port=5000)

