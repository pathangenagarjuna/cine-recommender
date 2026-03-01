Cine-Recommender

An AI-powered Movie Recommendation System built using Machine Learning and deployed on Streamlit Cloud.

🌐 Live App:  
https://cine-recommender-lyl7pfw2amwzjuocmjwfhf.streamlit.app/

---

🚀 Features

- 🎥 Content-Based Movie Recommendation
- 📊 Cosine Similarity based matching
- ⭐ Movie ratings & release dates
- 🖼️ Live posters fetched from TMDB API
- 🔥 Trending movies section
- ⚡ Memory-optimized vector similarity computation
- ☁️ Fully deployed on Streamlit Cloud

---

🧠 How It Works

1. Movie features such as overview, genres, and keywords were combined.
2. Text data was transformed into numerical vectors using **CountVectorizer (Bag-of-Words model)**.
3. Cosine similarity is computed dynamically between selected movie and all other movies.
4. Top 5 most similar movies are recommended.
5. Movie details are fetched live from the TMDB API.

---

🏗️ Tech Stack

- Python
- Streamlit
- Scikit-Learn
- Pandas
- TMDB API
- Joblib
- GitHub
- Streamlit Cloud

---

📂 Project Structure


cine-recommender/
│
├── app.py
├── movie_dict.pkl
├── vectors.pkl
├── requirements.txt
└── README.md


---

⚙️ Installation (Run Locally)

bash
git clone https://github.com/pathangenagarjuna/cine-recommender.git
cd cine-recommender
pip install -r requirements.txt
streamlit run app.py


---

🔐 Environment Variables

Create a `.env` file or set environment variable:

API_KEY=your_tmdb_api_key

---

🌍 Deployment

This app is deployed on **Streamlit Cloud** and automatically updates when new changes are pushed to GitHub.

---

👨‍💻 Developed By

**Nagarjuna Pathange**
Machine Learning Enthusiast, 
Computer Science Student,
Movie Enthusiast

---

⭐ Future Improvements

* Add collaborative filtering
* Hybrid recommendation model
* Genre-based filtering
* Dark theme UI
* User watchlist


📌 License

This project is for educational and demonstration purposes.
l me what you want next 🚀
```
