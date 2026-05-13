from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
from marshmallow import ValidationError
from dotenv import load_dotenv
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from functools import wraps
import os

from models import Song, User
from auth import hash_password, verify_password, create_token, verify_token
from errors import error_response
from schemas import LoginSchema, DataQuerySchema, AddSongSchema

load_dotenv() #charge les variables de .env

app = Flask(__name__)
#active Swagger
Swagger(app, template={"swagger": "2.0", "info": {"title": "Spotify API", "version": "1.0"}})

# --- Base de données ---
engine = create_engine("sqlite:///streaming.db")
Song.metadata.create_all(engine) #création des tables si elles n'existent pas
User.metadata.create_all(engine) #Ajout Postman
Session = sessionmaker(bind=engine)

# --- Rate limiting (limite les requêtes par @IP) ---
limiter = Limiter(get_remote_address, app=app)


# --- Décorateur JWT (protège une route) ---
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth.replace("Bearer ", "")
        payload = verify_token(token)#vérifie le token via auth.py
        if not payload: #si token invalide
            return error_response("unauthorized", "Token invalide ou expiré", 401)
        request.user = payload #stocke le payload pour l'uliliser dans la route
        return f(*args, **kwargs)
    return wrapper



# POST /api/login

@app.route("/api/login", methods=["POST"])
@limiter.limit("5 per minute") #pour brute force
def login():
    """
    Authentification utilisateur
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [username, password]
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200: description: JWT renvoyé
      401: description: Identifiants incorrects
      422: description: Validation échouée
      429: description: Trop de tentatives
    """
    """try:
        #valide le login envoyé avec LoginSchema
        data = LoginSchema().load(request.get_json() or {})
    except ValidationError as e:
        return error_response("validation_failed", e.messages, 422)#si la validation echoue

    # Ici tu vérifieras l'utilisateur en base quand tu auras un modèle User
    # Pour l'instant, retour d'exemple
    return error_response("unauthorized", "Identifiants incorrects", 401)
    """
    #Ajout Postman
    try:
        data = LoginSchema().load(request.get_json() or {})
    except ValidationError as e:
        return error_response("validation_failed", e.messages, 422)

    username = data["username"]
    password = data["password"]

    session = Session()

    # Vérifier si l'utilisateur existe
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return error_response("unauthorized", "Utilisateur introuvable", 401)

    # Vérifier le mot de passe
    if not verify_password(password, user.password_hash):
        return error_response("unauthorized", "Mot de passe incorrect", 401)

    # Générer un token JWT
    token = create_token(user.id)

    return jsonify({
        "message": "Connexion réussie",
        "token": token
    }), 200


# -----------------------------------------------------------------------
# GET /api/data
# -----------------------------------------------------------------------
@app.route("/api/data", methods=["GET"])
@jwt_required
def get_data():
    """
    Retourne les chansons filtrables
    ---
    parameters:
      - name: limit
        in: query
        type: integer
        default: 50
      - name: offset
        in: query
        type: integer
        default: 0
      - name: artist
        in: query
        type: string
    responses:
      200: description: Liste des chansons
      401: description: Non authentifié
      422: description: Paramètres invalides
    """
    try:
        params = DataQuerySchema().load(request.args)
    except ValidationError as e:
        return error_response("validation_failed", e.messages, 422)

    session = Session()
    try:
        query = session.query(Song)

        if params.get("artist"):
            query = query.filter(Song.Artist.ilike(f"%{params['artist']}%"))

        total = query.count()
        chansons = query.offset(params["offset"]).limit(params["limit"]).all()

        result = [{
            "id": c.id,
            "Track": c.Track,
            "Artist": c.Artist,
            "Album_Name": c.Album_Name,
            "Spotify_Streams": c.Spotify_Streams
        } for c in chansons]

        return jsonify({"total": total, "data": result}), 200

    finally:
        session.close()


# -----------------------------------------------------------------------
# GET /api/insights
# -----------------------------------------------------------------------
@app.route("/api/insights", methods=["GET"])
@jwt_required
def get_insights():
    """
    Agrégations et statistiques sur les chansons
    ---
    responses:
      200: description: Statistiques globales
      401: description: Non authentifié
    """
    session = Session()
    try:
        total_chansons = session.query(func.count(Song.id)).scalar()
        total_streams = session.query(func.sum(Song.Spotify_Streams)).scalar() or 0
        moyenne_streams = session.query(func.avg(Song.Spotify_Streams)).scalar() or 0

        top_artistes = (
            session.query(Song.Artist, func.sum(Song.Spotify_Streams).label("streams"))
            .group_by(Song.Artist)
            .order_by(func.sum(Song.Spotify_Streams).desc())
            .limit(5)
            .all()
        )

        return jsonify({
            "total_chansons": total_chansons,
            "total_streams": int(total_streams),
            "moyenne_streams": round(float(moyenne_streams), 0),
            "top_5_artistes": [
                {"artist": a, "streams": int(s)} for a, s in top_artistes
            ]
        }), 200

    finally:
        session.close()


# -----------------------------------------------------------------------
# GET /api/artists/<nom_artiste>
# -----------------------------------------------------------------------
@app.route("/api/artists/<nom_artiste>", methods=["GET"])
@jwt_required
def get_artists(nom_artiste):
    """
    Recherche les chansons d'un artiste
    ---
    parameters:
      - name: nom_artiste
        in: path
        type: string
        required: true
    responses:
      200: description: Liste des chansons de l'artiste
      401: description: Non authentifié
      404: description: Artiste non trouvé
    """
    session = Session()
    try:
        result = session.query(Song).filter(Song.Artist.ilike(f"%{nom_artiste}%")).all()

        if not result:
            return error_response("not_found", "Artiste non trouvé", 404)

        return jsonify([{
            "id": c.id,
            "Track": c.Track,
            "Artist": c.Artist,
            "Album_Name": c.Album_Name,
            "Spotify_Streams": c.Spotify_Streams
        } for c in result]), 200

    finally:
        session.close()


# -----------------------------------------------------------------------
# POST /api/add
# -----------------------------------------------------------------------
@app.route("/api/add", methods=["POST"])
@jwt_required
def add_song():
    """
    Ajoute une chanson en base
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [Track, Artist, Album_Name, Spotify_Streams]
          properties:
            Track:
              type: string
            Artist:
              type: string
            Album_Name:
              type: string
            Spotify_Streams:
              type: integer
    responses:
      201: description: Chanson ajoutée
      401: description: Non authentifié
      422: description: Validation échouée
    """
    try:
        data = AddSongSchema().load(request.get_json() or {})
    except ValidationError as e:
        return error_response("validation_failed", e.messages, 422)

    session = Session()
    try:
        nouvelle_chanson = Song(
            Track=data["Track"],
            Artist=data["Artist"],
            Album_Name=data["Album_Name"],
            Spotify_Streams=data["Spotify_Streams"]
        )
        session.add(nouvelle_chanson)
        session.commit()
        return jsonify({"message": "Chanson ajoutée avec succès"}), 201

    except Exception as e:
        session.rollback()
        return error_response("server_error", str(e), 500)

    finally:
        session.close()


#Ajout Postman
@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = LoginSchema().load(request.get_json() or {})
    except ValidationError as e:
        return error_response("validation_failed", e.messages, 422)


    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return error_response("validation_failed", "username et password requis", 400)

    session = Session()

    # Vérifier si l'utilisateur existe déjà
    if session.query(User).filter_by(username=username).first():
        return error_response("user_exists", "Utilisateur déjà existant", 400)

    # Créer l'utilisateur
    user = User(
        username=username,
        password_hash=hash_password(password)
    )

    session.add(user)
    session.commit()

    return jsonify({"message": "Utilisateur créé avec succès"}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)