import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Song

# ── Configuration de la page ──────────────────────────────────────
st.set_page_config(
    page_title="L'influence des réseaux sur la musique en 2024",
    page_icon="🎵",
    layout="wide"
)

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1ed760;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    [data-testid="stSidebar"] .stMultiSelect > div,
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"],
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="input"] {
        background-color: white !important;
        border-color: white !important;
    }
    [data-testid="stSidebar"] button {
        background-color: white !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── Connexion à la base de données ────────────────────────────────
engine = create_engine("sqlite:///streaming.db")
Session = sessionmaker(bind=engine)

# ── Sidebar : Filtres ─────────────────────────────────────────────
st.sidebar.header("🎛️ Filtres")

session = Session()
artists = sorted([a[0] for a in session.query(Song.Artist).distinct().all() if a[0]])
session.close()

artist_filter = st.sidebar.multiselect("Artiste(s)", options=artists)

session = Session()

if artist_filter:
    tracks = sorted([
        t[0] for t in session.query(Song.Track)
        .filter(Song.Artist.in_(artist_filter))
        .distinct().all() if t[0]
    ])
else:
    tracks = sorted([t[0] for t in session.query(Song.Track).distinct().all() if t[0]])
session.close()

song_filter = st.sidebar.multiselect("Chanson(s)", options=tracks)

# ── Requête filtrée ───────────────────────────────────────────────
session = Session()
query = session.query(Song)

if artist_filter:
    query = query.filter(Song.Artist.in_(artist_filter))
if song_filter:
    query = query.filter(Song.Track.in_(song_filter))

chansons = query.all()
session.close()

# ── Helper : conversion en millions ──────────────────────────────
def en_millions(valeur):
    return round((valeur or 0) / 1_000_000, 2)

# ── Titre principal ───────────────────────────────────────────────
st.title("🎵 L'influence des réseaux sociaux sur la musique en 2024")
st.write("Analyse des liens entre TikTok, YouTube, Shazam et les streams Spotify.")
st.divider()

# ── KPIs ──────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

total_streams_M = round(sum(c.Spotify_Streams or 0 for c in chansons) / 1_000_000, 2)
nb_chansons = len(chansons)
nb_artistes = len(set(c.Artist for c in chansons if c.Artist))

if chansons:
    top_tiktok_chanson = max(chansons, key=lambda c: c.TikTok_Likes or 0).Track
    top_tiktok_artiste = max(
        set(c.Artist for c in chansons if c.Artist),
        key=lambda a: sum(c.TikTok_Likes or 0 for c in chansons if c.Artist == a)
    )
else:
    top_tiktok_chanson = "N/A"
    top_tiktok_artiste = "N/A"

col1.metric("🎧 Total Streams", f"{total_streams_M:,} M")
col2.metric("🎵 Chansons", nb_chansons)
col3.metric("🎤 Artistes", nb_artistes)
col4.metric("🔥 Top TikTok chanson", top_tiktok_chanson)
col5.metric("⭐ Top TikTok artiste", top_tiktok_artiste)

st.divider()

# ── Onglets ───────────────────────────────────────────────────────
onglet1, onglet2, onglet3 = st.tabs(["🏆 Top Artistes", "🎵 Spotify vs TikTok", "🔮 Meilleur Prédicteur"])

# ── Onglet 1 : Top Artistes ───────────────────────────────────────
with onglet1:

    st.header("🎤 Top 10 artistes par Spotify Streams ")
    session = Session()
    query2 = session.query(Song)
    if artist_filter:
        query2 = query2.filter(Song.Artist.in_(artist_filter))
    if song_filter:
        query2 = query2.filter(Song.Track.in_(song_filter))

    top10_artistes = (
        query2.with_entities(Song.Artist, func.sum(Song.Spotify_Streams))
        .group_by(Song.Artist)
        .order_by(func.sum(Song.Spotify_Streams).desc())
        .limit(10).all()
    )
    session.close()

    df_top10 = pd.DataFrame(top10_artistes, columns=["Artist", "Total_Streams_M"])
    df_top10["Total_Streams_M"] = df_top10["Total_Streams_M"].apply(en_millions)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_top10,
                 x="Total_Streams_M",
                   y="Artist",
                     ax=ax,
                       color="#1ed760")
    ax.set_title("Top 10 Artistes par Spotify Streams")
    ax.set_xlabel("Total Spotify Streams (en millions)")
    ax.set_ylabel("Artiste")
    st.pyplot(fig)

    st.header("🎵 Top 10 chansons par Spotify Streams")
    session = Session()
    query3 = session.query(Song)
    if artist_filter:
        query3 = query3.filter(Song.Artist.in_(artist_filter))
    if song_filter:
        query3 = query3.filter(Song.Track.in_(song_filter))

    top10_chansons = (
    query3.with_entities(Song.Track, Song.Artist, func.sum(Song.Spotify_Streams))
    .group_by(Song.Track, Song.Artist)
    .order_by(func.sum(Song.Spotify_Streams).desc())
    .limit(10).all()
)

    df_top10_chansons = pd.DataFrame(top10_chansons, columns=["Track", "Artist", "Total_Streams_M"])
    df_top10_chansons["Total_Streams_M"] = df_top10_chansons["Total_Streams_M"].apply(en_millions)
    df_top10_chansons["Label"] = df_top10_chansons["Track"] + " — " + df_top10_chansons["Artist"]

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_top10_chansons,
                x="Total_Streams_M",
                y="Label",
                ax=ax2,
                color="#1ed760")
    ax2.set_title("Top 10 Chansons par Spotify Streams")
    ax2.set_xlabel("Total Spotify Streams (en millions)")
    ax2.set_ylabel("")
    st.pyplot(fig2)

# ── Onglet 2 : Spotify vs TikTok ─────────────────────────────────
with onglet2:
 
    st.header("TikTok vs Spotify")
    st.write("Est-ce que les sons viraux TikTok dominent vraiment Spotify ?")
 
    # Heatmap de corrélation
    df_corr = pd.DataFrame({
        "Spotify_Streams (M)": [en_millions(c.Spotify_Streams) for c in chansons],
        "TikTok_Views (M)":    [en_millions(c.TikTok_Views) for c in chansons],
        "TikTok_Likes (M)":    [en_millions(c.TikTok_Likes) for c in chansons],
    })
 
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    cmap_custom = LinearSegmentedColormap.from_list("spotify", ["#2af0ea", "#fe2858"])
    sns.heatmap(df_corr.corr(), 
                annot=True, 
                fmt=".2f", 
                cmap=cmap_custom, 
                ax=ax3)
    ax3.set_title("Corrélation TikTok / Spotify (en millions)")
    st.pyplot(fig3)
 
    #st.divider()


    # Scatter plot + coefficient
    tiktok_views = [en_millions(c.TikTok_Views) for c in chansons]
    spotify_streams = [en_millions(c.Spotify_Streams) for c in chansons]

    n = len(tiktok_views)
    moy_t = sum(tiktok_views) / n
    moy_s = sum(spotify_streams) / n
    cov = sum((tiktok_views[i] - moy_t) * (spotify_streams[i] - moy_s) for i in range(n))
    std_t = (sum((x - moy_t)**2 for x in tiktok_views))**0.5
    std_s = (sum((x - moy_s)**2 for x in spotify_streams))**0.5
    corr = cov / (std_t * std_s)

    #st.metric("Coefficient de corrélation TikTok Views / Spotify Streams", f"{corr:.3f}")
    st.info("Une corrélation proche de 0 signifie que la viralité TikTok ne prédit pas le succès Spotify.")

    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.regplot(
        x=tiktok_views,
        y=spotify_streams,
        ax=ax4,
        ci=None,
        scatter_kws={"alpha": 0.3, "color": "#2af0ea"},
        line_kws={"color": "#fe2858", "linewidth": 2}
    )
    ax4.set_xlabel("TikTok Views (en millions)")
    ax4.set_ylabel("Spotify Streams (en millions)")
    ax4.set_title("TikTok Views vs Spotify Streams")
    st.pyplot(fig4)




# ── Onglet 3 : Meilleur Prédicteur ───────────────────────────────
with onglet3:

    st.header("Quel réseau prédit le mieux les streams Spotify ?")

    st.info("Plus le coefficient est proche de 1, plus le réseau est un bon prédicteur du succès Spotify.")

    df_pred = pd.DataFrame({
        "Spotify_Streams (M)": [en_millions(c.Spotify_Streams) for c in chansons],
        "YouTube_Views (M)":   [en_millions(c.YouTube_Views) for c in chansons],
        "YouTube_Likes (M)":   [en_millions(c.YouTube_Likes) for c in chansons],
        "TikTok_Views (M)":    [en_millions(c.TikTok_Views) for c in chansons],
        "TikTok_Likes (M)":    [en_millions(c.TikTok_Likes) for c in chansons],
        "Shazam_Counts (M)":   [en_millions(c.Shazam_Counts) for c in chansons],
        "AirPlay_Spins (M)":   [en_millions(c.AirPlay_Spins) for c in chansons],
    })

    correlations = df_pred.drop(columns=["Spotify_Streams (M)"]).corrwith(df_pred["Spotify_Streams (M)"]).sort_values(ascending=False)
    meilleur = correlations.idxmax()


    fig5, ax5 = plt.subplots(figsize=(8, 4))
    correlations.plot(kind="bar",
                      ax=ax5,
                      color="#C4302B")
    ax5.set_title("Corrélation de chaque réseau avec Spotify Streams")
    ax5.set_ylabel("Coefficient de corrélation")
    ax5.set_xticklabels(correlations.index, rotation=45, ha="right")
    st.pyplot(fig5)

