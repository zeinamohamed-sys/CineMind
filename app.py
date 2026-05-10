import importlib.util
import subprocess
import sys


def ensure_package(package_name: str, import_name: Optional[str] = None):
    """Install missing packages automatically when possible."""
    target = import_name or package_name
    if importlib.util.find_spec(target) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])


# Auto-install required libraries
ensure_package("streamlit")
ensure_package("textblob")

import os
from collections import Counter
from typing import Optional

import streamlit as st
from textblob import TextBlob

st.set_page_config(
    page_title="CineMind",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

MOVIES = [
    {
        "title": "Inception",
        "genre": "Sci-Fi",
        "description": "A skilled thief enters layered dreams to steal secrets and plant a transformative idea.",
    },
    {
        "title": "The Dark Knight",
        "genre": "Action",
        "description": "Batman faces the Joker, a chaotic mastermind determined to push Gotham into anarchy.",
    },
    {
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "description": "A team travels through a wormhole in search of a new home for humanity.",
    },
    {
        "title": "Titanic",
        "genre": "Romance",
        "description": "Two young lovers meet aboard the ill-fated ship and share an unforgettable story.",
    },
    {
        "title": "The Shawshank Redemption",
        "genre": "Drama",
        "description": "A banker sentenced to life in prison builds hope, friendship, and a quiet plan for freedom.",
    },
    {
        "title": "The Godfather",
        "genre": "Crime",
        "description": "The aging patriarch of a powerful mafia family hands control to his reluctant son.",
    },
    {
        "title": "La La Land",
        "genre": "Musical",
        "description": "An aspiring actress and a jazz musician chase dreams and love in Los Angeles.",
    },
    {
        "title": "Parasite",
        "genre": "Thriller",
        "description": "A poor family slowly infiltrates a wealthy household, sparking dangerous consequences.",
    },
    {
        "title": "Avengers: Endgame",
        "genre": "Superhero",
        "description": "The surviving heroes gather for one final mission to undo a universe-shattering tragedy.",
    },
    {
        "title": "Spider-Man: Into the Spider-Verse",
        "genre": "Animation",
        "description": "Miles Morales discovers a multiverse of Spider-heroes and grows into his own identity.",
    },
    {
        "title": "The Conjuring",
        "genre": "Horror",
        "description": "Paranormal investigators help a family terrorized by a dark supernatural force.",
    },
    {
        "title": "Coco",
        "genre": "Animation",
        "description": "A music-loving boy journeys into the Land of the Dead to uncover his family history.",
    },
    {
        "title": "Whiplash",
        "genre": "Drama",
        "description": "A driven drummer faces a brutal instructor who pushes ambition to the edge.",
    },
    {
        "title": "Get Out",
        "genre": "Horror",
        "description": "A weekend visit to meet a girlfriend's family turns into a chilling psychological trap.",
    },
    {
        "title": "Mad Max: Fury Road",
        "genre": "Action",
        "description": "A relentless desert chase becomes a rebellion against a tyrannical warlord.",
    },
    {
        "title": "The Notebook",
        "genre": "Romance",
        "description": "A lifelong love story unfolds through memory, separation, and emotional reunion.",
    },
    {
        "title": "Knives Out",
        "genre": "Mystery",
        "description": "A witty detective investigates the suspicious death of a famous crime novelist.",
    },
    {
        "title": "Dune",
        "genre": "Adventure",
        "description": "A young nobleman embraces destiny on a desert planet at the center of a galactic conflict.",
    },
    {
        "title": "The Social Network",
        "genre": "Biography",
        "description": "The rise of a tech empire reveals ambition, betrayal, and the cost of innovation.",
    },
    {
        "title": "Toy Story",
        "genre": "Family",
        "description": "A group of toys comes alive when humans are away, learning loyalty and friendship.",
    },
]

GENRES = sorted({movie["genre"] for movie in MOVIES})


def load_local_image(path: str) -> bool:
    if os.path.exists(path):
        st.image(path, use_container_width=True)
        return True
    return False


@st.cache_data
def get_movies_by_genre(genre: str):
    return [movie for movie in MOVIES if movie["genre"] == genre]


@st.cache_data
def get_genre_stats():
    return Counter(movie["genre"] for movie in MOVIES)



def analyze_sentiment(review_text: str):
    blob = TextBlob(review_text)
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        label = "Positive"
        emoji = "🌟"
        color = "#00d26a"
        message = "This review has a strong positive vibe."
    elif polarity < -0.2:
        label = "Negative"
        emoji = "⚠️"
        color = "#ff5c5c"
        message = "This review feels critical or disappointed."
    else:
        label = "Neutral"
        emoji = "🎭"
        color = "#f5c542"
        message = "This review appears balanced or mixed."

    return {
        "label": label,
        "emoji": emoji,
        "color": color,
        "score": round(polarity, 3),
        "message": message,
    }


st.markdown(
    """
    <style>
        :root {
            --bg: #0b0b0f;
            --card: rgba(255, 255, 255, 0.06);
            --card-2: rgba(255, 255, 255, 0.08);
            --text: #f5f7fa;
            --muted: #b4b7c3;
            --accent: #e50914;
            --accent-2: #8b0000;
            --success: #00d26a;
            --warning: #f5c542;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(229, 9, 20, 0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(80, 0, 0, 0.18), transparent 25%),
                linear-gradient(180deg, #08080b 0%, #111114 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1300px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(18,18,24,0.98), rgba(10,10,14,0.98));
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        h1, h2, h3, h4, p, label, div {
            color: var(--text);
        }

        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 24px;
            padding: 2rem;
            min-height: 300px;
            background:
                linear-gradient(90deg, rgba(6,6,8,0.92) 0%, rgba(6,6,8,0.78) 45%, rgba(6,6,8,0.35) 100%),
                url('banner.png');
            background-size: cover;
            background-position: center;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 20px 45px rgba(0,0,0,0.35);
            margin-bottom: 1rem;
        }

        .hero::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(229,9,20,0.18), transparent 45%);
            pointer-events: none;
        }

        .hero-title {
            font-size: 3rem;
            line-height: 1.05;
            font-weight: 800;
            margin-bottom: 0.75rem;
            letter-spacing: -0.03em;
        }

        .hero-sub {
            max-width: 750px;
            color: var(--muted);
            font-size: 1.05rem;
            line-height: 1.7;
        }

        .glass-card {
            background: var(--card);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 1.2rem;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25);
            backdrop-filter: blur(10px);
        }

        .metric-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            min-height: 120px;
        }

        .metric-label {
            font-size: 0.9rem;
            color: var(--muted);
            margin-bottom: 0.4rem;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 800;
            color: #ffffff;
        }

        .movie-card {
            background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 1rem;
            min-height: 190px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            margin-bottom: 1rem;
        }

        .movie-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 16px 35px rgba(0,0,0,0.3);
        }

        .badge {
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            background: rgba(229,9,20,0.16);
            color: #ff7b81;
            border: 1px solid rgba(229,9,20,0.35);
            margin-bottom: 0.75rem;
        }

        .movie-title {
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 0.55rem;
        }

        .movie-desc {
            color: var(--muted);
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .sentiment-box {
            border-radius: 20px;
            padding: 1.2rem;
            border: 1px solid rgba(255,255,255,0.08);
            background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.03));
            margin-top: 1rem;
        }

        .footer-note {
            text-align: center;
            color: var(--muted);
            padding: 1rem 0 0.5rem 0;
            font-size: 0.9rem;
        }

        .stButton > button, .stDownloadButton > button {
            background: linear-gradient(90deg, #e50914, #b20710);
            color: white;
            border: none;
            border-radius: 999px;
            padding: 0.65rem 1.2rem;
            font-weight: 700;
        }

        .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
            background-color: rgba(255,255,255,0.04) !important;
            color: white !important;
            border-radius: 14px !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255,255,255,0.05);
            border-radius: 999px;
            padding: 0.35rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🎬 CineMind")
    if not load_local_image("logo.png"):
        st.markdown(
            """
            <div class='glass-card' style='text-align:center;'>
                <h2 style='margin-bottom:0.2rem;'>CineMind</h2>
                <p style='color:#b4b7c3; margin:0;'>Drop logo.png beside app.py to brand the app.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Discover")
    selected_sidebar_genre = st.selectbox("Browse by genre", ["All"] + GENRES)
    if selected_sidebar_genre == "All":
        browse_pool = MOVIES
    else:
        browse_pool = get_movies_by_genre(selected_sidebar_genre)

    st.markdown(f"**Available Titles:** {len(browse_pool)}")
    st.markdown("---")
    st.markdown(
        "CineMind is a plug-and-play movie intelligence dashboard with instant recommendations and review sentiment insights."
    )

st.markdown(
    """
    <div class="hero">
        <div style="position:relative; z-index:2; max-width: 780px;">
            <div class="badge">NETFLIX-STYLE • DARK MODE • AI-POWERED</div>
            <div class="hero-title">CineMind</div>
            <div class="hero-sub">
                Explore a built-in movie universe, analyze the mood of audience reviews with AI sentiment analysis,
                and get instant genre-based recommendations — all inside one sleek cinematic dashboard.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

stats = get_genre_stats()
col1, col2, col3, col4 = st.columns(4)
col1.markdown(
    f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Movies</div>
        <div class='metric-value'>{len(MOVIES)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
col2.markdown(
    f"""
    <div class='metric-card'>
        <div class='metric-label'>Genres</div>
        <div class='metric-value'>{len(GENRES)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
col3.markdown(
    f"""
    <div class='metric-card'>
        <div class='metric-label'>Top Genre</div>
        <div class='metric-value'>{stats.most_common(1)[0][0]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
col4.markdown(
    f"""
    <div class='metric-card'>
        <div class='metric-label'>Ready to Demo</div>
        <div class='metric-value'>100%</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

tab1, tab2, tab3 = st.tabs(["🎯 Recommendations", "🧠 Sentiment Lab", "🎞️ Movie Library"])

with tab1:
    st.markdown("### Find your next movie")
    st.markdown("Choose a genre and CineMind will instantly recommend titles from the built-in catalog.")

    genre_choice = st.selectbox("Select genre for recommendations", GENRES, key="genre_recommend")
    recommendations = get_movies_by_genre(genre_choice)

    rec_cols = st.columns(2)
    for idx, movie in enumerate(recommendations):
        with rec_cols[idx % 2]:
            st.markdown(
                f"""
                <div class='movie-card'>
                    <div class='badge'>{movie['genre']}</div>
                    <div class='movie-title'>{movie['title']}</div>
                    <div class='movie-desc'>{movie['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab2:
    st.markdown("### AI sentiment analysis for movie reviews")
    st.markdown("Paste or type a review below and CineMind will estimate its emotional tone using TextBlob.")

    sample_review = "An absolutely stunning film with breathtaking visuals and a deeply emotional story."
    review_text = st.text_area(
        "Your review",
        value=sample_review,
        height=180,
        placeholder="Type your movie review here...",
    )

    if st.button("Analyze Review"):
        result = analyze_sentiment(review_text)
        st.markdown(
            f"""
            <div class='sentiment-box'>
                <div class='badge'>SENTIMENT RESULT</div>
                <h3 style='margin: 0.2rem 0 0.4rem 0; color:{result['color']};'>
                    {result['emoji']} {result['label']}
                </h3>
                <p style='margin:0.2rem 0; color:#f5f7fa;'><strong>Polarity Score:</strong> {result['score']}</p>
                <p style='margin:0.4rem 0 0 0; color:#b4b7c3;'>{result['message']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab3:
    st.markdown("### Explore the internal movie dataset")
    st.markdown("This library is embedded directly inside the app, so no CSV or external data file is required.")

    library_pool = browse_pool
    lib_cols = st.columns(3)
    for idx, movie in enumerate(library_pool):
        with lib_cols[idx % 3]:
            st.markdown(
                f"""
                <div class='movie-card'>
                    <div class='badge'>{movie['genre']}</div>
                    <div class='movie-title'>{movie['title']}</div>
                    <div class='movie-desc'>{movie['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    """
    <div class='footer-note'>
        CineMind • Plug-and-Play Streamlit Movie Dashboard • Add banner.png and logo.png in the same folder for full branding.
    </div>
    """,
    unsafe_allow_html=True,
)
