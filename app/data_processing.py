import pandas as pd

def clean_spotify_data(csv_path):
    """
    On charge le dataset, nettoie les types numériques, supprime les colonnes trop vides,
    et remplace les valeurs manquantes numériques par la médiane pour qu'il n'y ait pas d'impact sur les prochaines mesures.
    """
    print(f"Chargement du fichier : {csv_path}...")
    
    # 1. Chargement 
    df = pd.read_csv(csv_path, encoding='latin-1')

    # 2. Nettoyage des virgules pour conversion en numérique
    colonnes_a_nettoyer = [
        'Spotify Streams', 'Spotify Playlist Count', 'Spotify Playlist Reach', 
        'YouTube Views', 'YouTube Likes', 'TikTok Likes', 'TikTok Views',
        'AirPlay Spins', 'Shazam Counts', 'All Time Rank'
    ]

    for col in colonnes_a_nettoyer:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
            
    # 3. Suppression des colonnes avec plus de 1000 valeurs nulles
    print("Vérification et suppression des colonnes trop vides...")
    colonnes_vides = df.columns[df.isnull().sum() > 1000]
    
    if len(colonnes_vides) > 0:
        print(f" -> Suppression des colonnes suivantes (> 1000 NaN) : {list(colonnes_vides)}")
        df = df.drop(columns=colonnes_vides)

    # 4. Remplacement des valeurs manquantes par la médiane
    colonnes_numeriques = df.select_dtypes(include=['float64', 'int64']).columns
    
    for col in colonnes_numeriques:
        # Calcul de la médiane en ignorant les valeurs manquantes
        mediane_col = df[col].median()
        # Remplacement des NaN par la médiane trouvée via fillna()
        df[col] = df[col].fillna(mediane_col)

    # 5. Modification du type de la colone "Release Date" en datetime
    if 'Release Date' in df.columns:
        df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
     

    print("Nettoyage OK")
    print(df.info())
    
    return df