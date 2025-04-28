# backend/app.py
# Importe les modules nécessaires
import os # Module pour interagir avec le système d'exploitation (pour les chemins de fichiers)
from flask import Flask, jsonify, request, send_from_directory # Ajout de send_from_directory
from flask_cors import CORS

# Initialise l'application Flask
# static_folder pointe vers le dossier où se trouvent les fichiers statiques (frontend)
# Il est relatif au dossier où CE script (app.py) est exécuté.
# '../frontend' signifie "remonte d'un niveau (sortir de backend/) puis va dans frontend/"
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
# Active CORS pour les routes API (toujours une bonne pratique)
# On restreint CORS aux routes commençant par /api/ pour plus de sécurité
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- Simulation de Base de Données ---
# Dans un vrai projet, ceci serait remplacé par une connexion à une base de données
# (PostgreSQL, MySQL, MongoDB...) en utilisant un ORM comme SQLAlchemy ou un driver direct.
# On utilise une simple liste de dictionnaires pour stocker les livres en mémoire.
books_db = [
    {"id": 1, "title": "Le Seigneur des Anneaux", "author": "J.R.R. Tolkien"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
    {"id": 3, "title": "Dune", "author": "Frank Herbert"}
]
# Variable pour générer le prochain ID unique pour les nouveaux livres
next_book_id = 4
# --- Fin de la Simulation de Base de Données ---

# --- Définition des Routes ---

# Route pour servir le fichier index.html du frontend à la racine '/'
# Cette route doit être définie AVANT les routes API si elles ont des chemins similaires
@app.route('/')
def serve_index():
    """Sert le fichier index.html du dossier frontend."""
    # send_from_directory cherche le fichier dans le static_folder défini lors de l'init de Flask
    # Ici, il cherchera donc dans '../frontend'
    print("Requête reçue pour servir index.html")
    # Vérifie si le static_folder est bien défini et existe
    if not app.static_folder or not os.path.isdir(app.static_folder):
         print(f"ERREUR: Le dossier static_folder '{app.static_folder}' n'est pas configuré ou n'existe pas.")
         return "Erreur de configuration serveur.", 500
    # Vérifie si index.html existe dans le static_folder
    index_path = os.path.join(app.static_folder, 'index.html')
    if not os.path.isfile(index_path):
         print(f"ERREUR: Le fichier 'index.html' n'a pas été trouvé dans {app.static_folder}")
         return "Fichier index.html non trouvé.", 404

    try:
        # Utilise static_folder défini dans Flask(__name__, static_folder=...)
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"Erreur inattendue lors de la tentative de servir index.html: {e}")
        # Retourne une erreur 500 (Internal Server Error) en cas de problème
        return "Erreur serveur interne.", 500


# --- Routes API (préfixées par /api pour éviter les conflits) ---

# Route pour obtenir la liste complète des livres (Méthode GET)
@app.route('/api/books', methods=['GET'])
def get_books():
    """Retourne la liste de tous les livres au format JSON."""
    print("Requête GET reçue pour /api/books")
    return jsonify(books_db)

# Route pour ajouter un nouveau livre (Méthode POST)
@app.route('/api/books', methods=['POST'])
def add_book():
    """Ajoute un nouveau livre à la 'base de données'."""
    global next_book_id
    print("Requête POST reçue pour /api/books")

    # Vérifie si la requête contient du JSON et les champs nécessaires
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        # Retourne une erreur 400 (Bad Request) si les données sont invalides
        return jsonify({"error": "Les champs 'title' et 'author' sont requis."}), 400

    # Crée le nouveau livre avec un ID unique
    new_book = {
        'id': next_book_id,
        'title': request.json['title'],
        'author': request.json['author']
    }
    # Ajoute le livre à notre "base de données" simulée
    books_db.append(new_book)
    # Incrémente l'ID pour le prochain ajout
    next_book_id += 1

    print(f"Livre ajouté : {new_book}") # Log
    # Retourne le livre ajouté et un statut 201 (Created)
    return jsonify(new_book), 201

# --- Démarrage du Serveur ---
# Ce bloc s'exécute seulement si le script est lancé directement (pas importé)
if __name__ == '__main__':
    # Vérifie si le dossier frontend (static_folder) existe bien à l'endroit attendu
    # Utilise app.static_folder qui a été configuré lors de l'initialisation de Flask
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
    # host='0.0.0.0' rend le serveur accessible depuis d'autres machines/conteneurs sur le réseau
    # port=5000 définit le port d'écoute
    # debug=True active le rechargement automatique et des messages d'erreur détaillés (utile en dev)
    app.run(debug=True, host='0.0.0.0', port=5000)

# Les lignes suivantes qui appartenaient à requirements.txt ont été supprimées de ce fichier.
# Assurez-vous qu'elles sont bien dans un fichier nommé 'requirements.txt'
# dans le même dossier 'backend'.
