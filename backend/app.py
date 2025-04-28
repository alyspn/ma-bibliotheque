# backend/app.py
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy # Importer SQLAlchemy

# --- Configuration ---
# Détermine le chemin absolu du dossier où se trouve ce script
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Configuration de la Base de Données ---
# Définit l'URI de la base de données SQLite
# 'sqlite:///' signifie que le fichier sera à la racine du projet.
# os.path.join(basedir, 'library.db') crée un fichier library.db dans le dossier backend
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'library.db')
# Désactive une fonctionnalité de SQLAlchemy qui n'est pas nécessaire et consomme des ressources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise l'extension SQLAlchemy avec l'application Flask
db = SQLAlchemy(app)
# --- Fin de la Configuration DB ---

# --- Modèle de Base de Données ---
# Définit la structure de la table 'book'
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Clé primaire auto-incrémentée
    title = db.Column(db.String(100), nullable=False) # Champ texte, ne peut pas être vide
    author = db.Column(db.String(100), nullable=False) # Champ texte, ne peut pas être vide

    # Méthode optionnelle pour convertir l'objet Book en dictionnaire (utile pour jsonify)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author
        }
# --- Fin du Modèle DB ---

# --- Initialisation de la Base de Données ---
# Cette fonction crée les tables si elles n'existent pas.
# Il faut la lancer une fois manuellement ou via une commande spécifique.
# Nous allons utiliser le contexte de l'application pour le faire.
with app.app_context():
    print("Vérification et création des tables de la base de données si nécessaire...")
    db.create_all() # Crée les tables définies dans les modèles (ici, la table 'book')
    print("Tables vérifiées/créées.")
# --- Fin Initialisation DB ---


# --- Définition des Routes ---

# Route pour servir le fichier index.html du frontend
@app.route('/')
def serve_index():
    """Sert le fichier index.html du dossier frontend."""
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


# --- Routes API Modifiées ---

# Route pour obtenir la liste complète des livres depuis la BDD
@app.route('/api/books', methods=['GET'])
def get_books():
    """Retourne la liste de tous les livres depuis la base de données."""
    print("Requête GET reçue pour /api/books")
    try:
        # Récupère tous les enregistrements de la table Book
        all_books = Book.query.all()
        # Convertit chaque objet Book en dictionnaire et crée une liste
        result = [book.to_dict() for book in all_books]
        return jsonify(result)
    except Exception as e:
        print(f"Erreur lors de la récupération des livres: {e}")
        return jsonify({"error": "Erreur serveur lors de la récupération des livres"}), 500


# Route pour ajouter un nouveau livre dans la BDD
@app.route('/api/books', methods=['POST'])
def add_book():
    """Ajoute un nouveau livre à la base de données."""
    print("Requête POST reçue pour /api/books")

    if not request.json or not 'title' in request.json or not 'author' in request.json:
        return jsonify({"error": "Les champs 'title' et 'author' sont requis."}), 400

    try:
        # Crée une nouvelle instance du modèle Book avec les données reçues
        new_book = Book(title=request.json['title'], author=request.json['author'])
        # Ajoute la nouvelle instance à la session SQLAlchemy
        db.session.add(new_book)
        # Valide (commit) les changements dans la base de données
        db.session.commit()

        print(f"Livre ajouté à la BDD : {new_book.to_dict()}")
        # Retourne le livre ajouté (converti en dict) et un statut 201
        return jsonify(new_book.to_dict()), 201
    except Exception as e:
        print(f"Erreur lors de l'ajout du livre: {e}")
        db.session.rollback() # Annule la transaction en cas d'erreur
        return jsonify({"error": "Erreur serveur lors de l'ajout du livre"}), 500

# --- Démarrage du Serveur ---
if __name__ == '__main__':
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

    print("Démarrage du serveur Flask sur http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

