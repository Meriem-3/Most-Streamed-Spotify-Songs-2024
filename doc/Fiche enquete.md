# 🎵 Fiche d'enquête — L'influence des réseaux sociaux sur la musique en 2024

---

## 1. Le dataset et la question

**Source** : Most Streamed Spotify Songs 2024 — Kaggle  
**Taille** : 4 600 chansons · 21 colonnes après nettoyage  
**Période** : Données 2024, toutes plateformes confondues  
**Plateformes couvertes** : Spotify, YouTube, TikTok, Shazam, Apple Music, Deezer, AirPlay

**Question de départ** :  
> Quel réseau social est le meilleur prédicteur de succès sur Spotify en 2024 ?

**Hypothèse testée** :  
> TikTok est le principal moteur de succès musical — les sons viraux TikTok dominent les streams Spotify.

---

## 2. La méthode

**Ce qu'on a calculé** :
- Corrélations entre chaque réseau (YouTube, TikTok, Shazam, AirPlay) et les Spotify Streams
- Visualisation de la relation TikTok Views / Spotify Streams via scatter plot et droite de régression
- Classement des meilleurs prédicteurs par coefficient de corrélation

**Comment** :
- Nettoyage des données avec Pandas (suppression colonnes > 1000 NaN, remplacement par médiane, conversion des types)
- Calcul des corrélations avec `corrwith()` et `corr()`
- Visualisations avec Matplotlib et Seaborn

**Biais identifiés** :
- Quelques artistes avec des caractères non-latins affichent des problèmes d'encodage — sans impact sur l'analyse numérique
- Les valeurs manquantes ont été remplacées par la médiane, ce qui peut légèrement atténuer les corrélations extrêmes
- Le dataset couvre uniquement les chansons les plus streamées — les artistes émergents ne sont pas représentés

---

## 3. Les conclusions

**1. Spotify domine le streaming musical**  
Avec 600 à 675 millions d'utilisateurs actifs, Spotify est de loin la première plateforme de streaming musical pur — loin devant Apple Music (93M) et Deezer (10M).

**2. TikTok ne prédit pas le succès Spotify**  
La corrélation TikTok Views / Spotify Streams est proche de 0. Le scatter plot confirme visuellement que les chansons qui explosent sur TikTok ne sont pas celles qui dominent les streams. La viralité ne se convertit pas en écoutes durables.

**3. YouTube est la piste à creuser**  
La corrélation YouTube / Spotify est significativement plus forte que TikTok / Spotify. Les artistes qui soignent leur présence YouTube semblent mieux performer sur Spotify — une piste concrète pour les professionnels du secteur.

**Limites** :
- On ne peut pas établir de causalité — une forte corrélation YouTube/Spotify peut s'expliquer par un troisième facteur (notoriété globale de l'artiste)
- L'analyse porte sur le volume de streams, pas sur la fidélisation des auditeurs

---

## 4. L'ingénierie

**Stack** :
- Python 3.11 · Flask · Streamlit · SQLite via SQLAlchemy ORM · Pandas · Seaborn

**Sécurité** :
- Mots de passe hashés avec bcrypt (rounds=12) — résistant aux rainbow tables
- Tokens JWT signés (HS256) avec expiration courte, secret dans `.env`
- Zéro SQL brut — ORM uniquement, protection native contre les injections SQL
- Validation systématique des entrées avec Marshmallow
- Rate limiting sur `/api/login` (5 req/min) — protection brute force