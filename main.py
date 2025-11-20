import os
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -------------------------------
# Paths setup
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # script folder
MOVIES_CSV = os.path.join(BASE_DIR, "movies_data.csv")
FEATURES_PKL = os.path.join(BASE_DIR, "movies_features.pkl")
KNN_PKL = os.path.join(BASE_DIR, "knn_movie_recommender.pkl")

# -------------------------------
# Load the data + KNN model
# -------------------------------
@st.cache_data
def load_data():
    # Check files exist
    for path in [MOVIES_CSV, FEATURES_PKL, KNN_PKL]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required file not found: {path}")

    # Load movies dataframe
    movies_df = pd.read_csv(MOVIES_CSV)

    # Load movie features (for KNN)
    movies_features = joblib.load(FEATURES_PKL)

    # Load pre-trained KNN model
    knn = joblib.load(KNN_PKL)

    return movies_df, movies_features, knn

# Load everything
movies_df, movies_features, knn = load_data()

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🎬 Movie Recommendation System")
st.write("Select a movie and get top 5 recommended movies using KNN.")

# Movie selection
movie_list = movies_df["title"].tolist()
selected_movie = st.selectbox("Select a movie:", movie_list)

# -------------------------------
# Recommendation Logic
# -------------------------------
def get_recommendations(movie_name, num_recs=5):
    try:
        # Find movie index
        movie_index = movies_df[movies_df["title"] == movie_name].index[0]

        # Get feature vector
        movie_vector = movies_features.iloc[movie_index].values.reshape(1, -1)

        # KNN search
        distances, indices = knn.kneighbors(movie_vector, n_neighbors=num_recs + 1)

        # Exclude the selected movie itself
        recommended_indices = indices.flatten()[1:]

        # Return recommended movie titles
        return movies_df.iloc[recommended_indices]["title"].tolist()

    except Exception as e:
        return ["Error: " + str(e)]

# -------------------------------
# Button → Recommend Movies
# -------------------------------
if st.button("🔍 Get Recommendations"):
    if selected_movie:
        st.subheader("📌 Recommended Movies:")
        recommendations = get_recommendations(selected_movie)

        for idx, movie in enumerate(recommendations, 1):
            st.write(f"**{idx}. {movie}**")
    else:
        st.warning("Please select a movie first.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Movie Recommender • KNN Model • Built with Streamlit")
