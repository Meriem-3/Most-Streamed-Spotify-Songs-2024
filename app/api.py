from flask import Flask, request, jsonify
from auth import hash_password, verify_password, create_token
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Song

load_dotenv()#lit le fichier .env

app = Flask(__name__)

#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#configurer la base de données
#DATABASE_URL = os.getenv("sqlite:///streaming.db")
engine = create_engine("sqlite:///streaming.db")
Song.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/api/songs", methods=["GET"])
def get_songs():
    
    session = Session()
    result = session.query(Song).all()
    print(result)
    liste_chansons=[]
    for chanson in result:
        liste_chansons.append({
            "id": chanson.id, 
            "title": chanson.Track,
            "artist": chanson.Artist, 
            "album": chanson.Album_Name})
    session.close()
    return jsonify(liste_chansons)


@app.route("/api/artists/<nom_artiste>", methods=["GET"])
def get_artists(nom_artiste):
    session = Session()
    result = session.query(Song).filter(Song.Artist.ilike(f"%{nom_artiste}%")).all()
    if not result:
        return jsonify({"message": "Artiste non trouvé"}), 404
    
    reponse = []
    for chanson in result:
        reponse.append({
            "id": chanson.id, 
            "title": chanson.Track,
            "artist": chanson.Artist, 
            "album": chanson.Album_Name,
            "nb_streams": chanson.Spotify_Streams})
    
    session.close()
    
    return jsonify(reponse)

@app.route("/api/add", methods=["POST"])
def add_data():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Aucune donnée fournie"}), 400
    
    try:
        session = Session()
        nouvelle_chanson = Song(
            title=data["Track"],
            artist=data["Artist"],
            album=data["Album_Name"],
            Spotify_Streams=data["Spotify_Streams"]
        )
        session.add(nouvelle_chanson)
        session.commit()
        session.close()
        return jsonify({"message": "Chanson ajoutée avec succès"}), 201
    except Exception as e:
        return jsonify({"message": f"Erreur lors de l'ajout de la chanson: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
