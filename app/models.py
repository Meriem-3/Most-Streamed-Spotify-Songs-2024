from sqlalchemy import Column, Integer, String, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'

    # Identifiant unique (clé primaire)
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Colonnes conservées après ton nettoyage (21 colonnes + ID)
    Track = Column(String) 
    Album_Name = Column(String)
    Artist = Column(String)
    Release_Date = Column(String)
    ISRC = Column(String)
    All_Time_Rank = Column(Integer)
    Track_Score = Column(Float)
    Spotify_Streams = Column(Integer)
    Spotify_Playlist_Count = Column(Float)
    Spotify_Playlist_Reach = Column(Float)
    Spotify_Popularity = Column(Float)
    YouTube_Views = Column(Float)
    YouTube_Likes = Column(Float)
    TikTok_Likes = Column(Float)
    TikTok_Views = Column(Float)
    Apple_Music_Playlist_Count = Column(Float)
    AirPlay_Spins = Column(Float)
    Deezer_Playlist_Count = Column(Float)
    Deezer_Playlist_Reach = Column(Float)
    Shazam_Counts = Column(Float)
    Explicit_Track = Column(Integer)

def init_db(db_url="sqlite:///streaming.db"):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    print("Base de données initialisée.")

if __name__ == "__main__":
    init_db()