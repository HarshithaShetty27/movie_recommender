import pandas as pd
import requests
import streamlit as st
import pickle

def fetch_poster(movie_title):
    api_key = "97e0fe90"
    response = requests.get(f"https://www.omdbapi.com/?t={movie_title}&apikey={api_key}")
    data = response.json()
    if 'Poster' in data and data['Poster']!='N/A':
        return data['Poster']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"  # Fallback image

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True, key= lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        # fetch poster from api
        recommended_movies_poster.append(fetch_poster(movie_title))
    return recommended_movies,recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Choose a movie for recommendations:",
    ["Select a movie"] + movies['title'].to_list()
)

if st.button("Recommend"):
    if selected_movie_name == "Select a movie":
        st.warning("Please select a movie before clicking Recommend.")
    else:
        names,posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(names[0])
            st.image(posters[0])

        with col2:
            st.text(names[1])
            st.image(posters[1])

        with col3:
            st.text(names[2])
            st.image(posters[2])

        with col4:
            st.text(names[3])
            st.image(posters[3])

        with col5:
            st.text(names[4])
            st.image(posters[4])





