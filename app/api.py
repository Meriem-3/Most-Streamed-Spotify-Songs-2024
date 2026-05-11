from flask import Flask, request, jsonify
from app.auth import hash_password, verify_password, create_token
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Songs

load_dotenv()#lit le fichier .env

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#configurer la base de données
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)()

@app.route("/api/songs", methods=["GET"])
def get_songs():
    session = Session()
    result = session.query("Songs").all()
    liste_chansons=[]
    for chanson in result:
        liste_chansons.append({
            "id": chanson.id, 
            "title": chanson.title,
            "artist": chanson.artist, 
            "album": chanson.album})
    session.close()
    return jsonify(liste_chansons)


@app.route("/api/artists/<nom_artiste>", methods=["GET"])
def get_artists():
    session = Session()
    result = session.query("Artists").all()
    return jsonify([artist.to_dict() for artist in result])

@app.route("/api/albums", methods=["GET"])
def get_albums():
    session = Session()
    result = session.query("Album_Name").all()
    return jsonify([album.to_dict() for album in result])

