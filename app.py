# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5535662c3f612adb6fa98f2fcbbb0941"
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#     recommended_movies = []
#     recommended_movies_posters =[]
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         #fetch poster from API
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies
# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl','rb'))
#
# st.title('Movie Recommendation System')
#
# selected_movie_name = st.selectbox('Select a movie you like',movies['title'].values)
#
# if st.button('Recommend'):
#     names,posters = recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.beta_columns(5)
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])
import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------- FETCH POSTER ---------------- #
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=5535662c3f612adb6fa98f2fcbbb0941"
#     response = requests.get(url)
#     data = response.json()
#
#     if data.get('poster_path'):
#         poster_path = data['poster_path']
#         return "https://image.tmdb.org/t/p/w500/" + poster_path
#     else:
#         return "https://via.placeholder.com/500x750?text=No+Image"
#
# # ---------------- RECOMMEND FUNCTION ---------------- #
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#
#     movies_list = sorted(
#         list(enumerate(distances)),
#         reverse=True,
#         key=lambda x: x[1]
#     )[1:6]
#
#     recommended_movies = []
#     recommended_posters = []
#
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies, recommended_posters
#
#
# # ---------------- LOAD DATA ---------------- #
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# # ---------------- STREAMLIT UI ---------------- #
# st.title('Movie Recommendation System')
#
# selected_movie_name = st.selectbox(
#     'Select a movie you like',
#     movies['title'].values
# )
#
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#
#     col1, col2, col3, col4, col5 = st.columns(5)
#
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])
import streamlit as st
import pickle
import pandas as pd
import requests

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Movie Recommender", layout="wide")

API_KEY = "5535662c3f612adb6fa98f2fcbbb0941"

# ================= LOAD DATA =================
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

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
        trending_movies.append({
            "title": movie["title"],
            "poster": "https://image.tmdb.org/t/p/w500/" + movie["poster_path"]
        })

    return trending_movies


# ================= RECOMMEND FUNCTION =================

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        score = i[1] * 100  # Keep full precision internally

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

st.sidebar.title("Movie Recommender")

st.sidebar.markdown("🍿 Discover. Explore. Enjoy.")
st.sidebar.markdown("Built with using Machine Learning concepts & Streamlit")
st.sidebar.markdown("**Developed by Nagarjuna**")

st.sidebar.markdown("---")

with st.sidebar.expander("ℹ️ How This System Works"):
    st.write("""
    • Movies were converted into numerical vectors using CountVectorizer.  
    • Cosine similarity matrix precomputed  
    • Top 5 most similar movies selected  
    • Movie details fetched using TMDB API  
    """)

# ================= MAIN TITLE =================

st.title(" Movie Recommendation System ")

# ================= RECOMMENDATION SECTION (TOP) =================

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

# ================= TRENDING SECTION (BOTTOM) =================

st.markdown("---")
st.subheader("🔥 Trending Movies Today")

trending = fetch_trending()
trend_cols = st.columns(5)

for i in range(len(trending)):
    with trend_cols[i]:
        st.image(trending[i]["poster"])
        st.caption(trending[i]["title"])