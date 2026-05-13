# 🎵 Most Streamed Spotify Songs 2024
> **L'influence des réseaux sociaux sur la musique en 2024**

Projet de data storytelling — Formation Python Semaine 2.  
**Question centrale : Quel réseau social prédit le mieux les streams Spotify ?**

---

## 📁 Structure du projet

```
Most-Streamed-Spotify-Songs-2024/
├── app/
│   ├── api.py              # API Flask — endpoints REST
│   ├── auth.py             # Sécurité — bcrypt, Fernet, JWT
│   ├── dashboard.py        # Dashboard Streamlit
│   ├── data_processing.py  # Nettoyage des données avec Pandas
│   ├── eda.ipynb           # Notebook d'exploration des données
│   ├── errors.py           # Réponses d'erreur structurées
│   ├── insert_data.py      # Insertion du CSV en base SQLite
│   ├── models.py           # Modèles SQLAlchemy
│   └── schemas.py          # Validation des entrées avec Marshmallow
├── data/
│   └── Most_Streamed_Spotify_Songs_2024.csv
├── doc/
│   └── requirements.txt
├── .gitignore
├── README.md
└── streaming.db
```

---

## 🚀 Installation

**1. Cloner le projet**
```bash
git clone <url-du-repo>
cd Most-Streamed-Spotify-Songs-2024
```

**2. Installer les dépendances**
```bash
pip install -r doc/requirements.txt
```

**3. Configurer les variables d'environnement**  
Créer un fichier `.env` à la racine :
```
SECRET_KEY=une-chaine-longue-et-aleatoire
JWT_SECRET=une-autre-chaine-aleatoire
FERNET_KEY=generer-avec-Fernet.generate_key()
```

**4. Insérer les données en base**
```bash
python app/insert_data.py
```

---

## ▶️ Lancer le projet

**API Flask**
```bash
python app/api.py
```
→ API disponible sur `http://localhost:5000`  
→ Documentation Swagger sur `http://localhost:5000/apidocs`

**Dashboard Streamlit**
```bash
python -m streamlit run app/dashboard.py
```
→ Dashboard disponible sur `http://localhost:8501`

---

## 🔌 Endpoints API

| Méthode | Route | Auth | Description |
|---------|-------|------|-------------|
| POST | `/api/login` | Non | Authentification — retourne un JWT |
| GET | `/api/data` | Oui | Chansons filtrables (limit, offset, artist) |
| GET | `/api/insights` | Oui | Agrégations et statistiques |
| GET | `/api/artists/<nom>` | Oui | Recherche par artiste |
| POST | `/api/add` | Oui | Ajouter une chanson |

---

## 📊 Dashboard

3 onglets d'analyse :

- **🏆 Top Artistes** — Top 10 artistes et chansons par streams Spotify
- **🎵 Spotify vs TikTok** — Heatmap de corrélation + scatter plot
- **🔮 Meilleur Prédicteur** — Quel réseau prédit le mieux le succès Spotify ?

Filtres interactifs par artiste et par chanson dans la sidebar.

---

## 🔒 Sécurité

- ORM SQLAlchemy uniquement — zéro SQL brut
- Mots de passe hashés avec **bcrypt** (rounds=12)
- Chiffrement des données sensibles avec **Fernet**
- Tokens **JWT** signés avec expiration courte
- Validation des entrées avec **Marshmallow**
- Rate limiting sur `/api/login` (5 requêtes/minute)

---

## 📦 Dataset

**Most Streamed Spotify Songs 2024** — Kaggle  
4 600 chansons · 21 colonnes après nettoyage  
Plateformes couvertes : Spotify, YouTube, TikTok, Shazam, Apple Music, Deezer, AirPlay

---

## 💡 Conclusions de l'analyse

- **Spotify domine** — de loin la première plateforme de streaming musical en volume d'écoutes
- **TikTok ≠ Spotify** — les données ne montrent pas de lien clair entre le succès sur TikTok et le succès sur Spotify. La viralité ne se convertit pas en streams durables.
- **YouTube, la piste à creuser** — la corrélation YouTube / Spotify est significativement plus forte que TikTok / Spotify. Les artistes qui soignent leur présence YouTube semblent mieux performer sur Spotify.