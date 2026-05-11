from sqlalchemy import create_engine
from app.data_processing import clean_spotify_data

def insert_to_db(csv_path, db_url="sqlite:///streaming.db"):
    """
    Récupère les données nettoyées et les insère dans la base de données via SQLAlchemy ORM.
    """
    # 1. Appel de ta fonction de nettoyage
    print("--- Étape 1 : Nettoyage des données ---")
    df_cleaned = clean_spotify_data(csv_path)
    
    # 2. Création de la connexion à la base de données via l'ORM
    print(f"\n--- Étape 2 : Connexion à la base de données ({db_url}) ---")
    # L'utilisation de create_engine garantit que nous respectons la consigne ORM Only
    engine = create_engine(db_url)
    
    # 3. Insertion sécurisée
    print("--- Étape 3 : Insertion des données dans la table 'songs' ---")
    # to_sql utilise l'ORM sous le capot, bloquant les injections SQL
    df_cleaned.to_sql(name='songs', con=engine, if_exists='replace', index=False)
    
    print(f"\n Succès : {len(df_cleaned)} morceaux ont été insérés dans la base de données !")

if __name__ == "__main__":
    FICHIER_CSV = "data/Most Streamed Spotify Songs 2024.csv"
    insert_to_db(FICHIER_CSV)