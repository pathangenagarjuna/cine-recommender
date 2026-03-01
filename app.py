import streamlit as st
import pickle
import pandas as pd
import requests
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Cine-Recommender", layout="wide")

# ================= API KEY =================
API_KEY = os.getenv("API_KEY")  # Set in Streamlit Cloud Secrets

# ================= LOAD DATA =================
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

vectors = joblib.load("vectors.pkl")

# ================= API FUNCTIONS =================

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()

    poster_path = data.get("poster_path")
    overview = data.get("overview", "No overview available")
    rating = data.get("vote_average", "N/A")
    release = data.get("release_date", "N/A")

    if poster_path:
        poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        poster_url = "https://via.placeholder.com/500x750?text=No+Image"

    return poster_url, overview, rating, release


def fetch_trending():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"
    data = requests.get(url).json()
    results = data.get("results", [])[:5]

    trending_movies = []

    for movie in results:
        poster_path = movie.get("poster_path")
        poster_url = (
            "https://image.tmdb.org/t/p/w500/" + poster_path
            if poster_path
            else "https://via.placeholder.com/500x750?text=No+Image"
        )

        trending_movies.append({
            "title": movie.get("title", "Unknown"),
            "poster": poster_url
        })

    return trending_movies


# ================= RECOMMEND FUNCTION =================

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    # Compute similarity dynamically (memory efficient)
    similarity_scores = cosine_similarity(
        vectors[movie_index], vectors
    ).flatten()

    movies_list = sorted(
        list(enumerate(similarity_scores)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        score = i[1] * 100

        poster, overview, rating, release = fetch_movie_details(movie_id)

        recommendations.append({
            "title": title,
            "poster": poster,
            "overview": overview,
            "rating": rating,
            "release": release,
            "score": score
        })

    return recommendations


# ================= SIDEBAR =================

st.sidebar.title("🎬 Cine-Recommender")

st.sidebar.markdown("🍿 Discover. Explore. Enjoy.")
st.sidebar.markdown("Built using Machine Learning & Streamlit")
st.sidebar.markdown("**Developed by Nagarjuna 🚀**")

st.sidebar.markdown("---")

with st.sidebar.expander("ℹ️ How This System Works"):
    st.write("""
    • Movies were converted into numerical vectors using CountVectorizer (Bag-of-Words).  
    • Cosine similarity is computed dynamically for the selected movie.  
    • Top 5 most similar movies are recommended.  
    • Movie details are fetched live from the TMDB API.
    """)

# ================= MAIN TITLE =================

st.title("Movie Recommendation System")

# ================= RECOMMENDATION SECTION =================

st.subheader("🎥 Select a Movie You Like")

selected_movie = st.selectbox(
    "",
    movies['title'].values
)

if st.button("Recommend Movies"):

    recommendations = recommend(selected_movie)

    st.subheader("🎯 Recommended For You")

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(recommendations[i]["poster"])
            st.markdown(f"**{recommendations[i]['title']}**")
            st.write(f"⭐ {recommendations[i]['rating']} / 10")
            st.write(f"📅 {recommendations[i]['release']}")
            st.write(f"📊 Similarity: {recommendations[i]['score']:.4f}%")
            st.caption(recommendations[i]["overview"][:150] + "...")

# ================= TRENDING SECTION =================

st.markdown("---")
st.subheader("🔥 Trending Movies Today")

trending = fetch_trending()
trend_cols = st.columns(5)

for i in range(len(trending)):
    with trend_cols[i]:
        st.image(trending[i]["poster"])
        st.caption(trending[i]["title"])

