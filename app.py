import streamlit as st
import pickle
import pandas as pd
import requests

def getPoster(movieId):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=929680f7a56b1562ed69c6f849fee84f&language=en-US'.format(movieId))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movieIndex = movies[movies['title'] == movie].index[0]
    distances = similarity[movieIndex]
    moviesList = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommendations = []
    posters = []
    for i in moviesList:
        movieId = movies.iloc[i[0]].movie_id
        recommendations.append(movies.iloc[i[0]].title)
        # to fetch poster from API
        posters.append(getPoster(movieId))
    return recommendations, posters
st.title('Movie Recommendation System')

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selectedMovieName = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values
)

st.write("You selected:", selectedMovieName)

if st.button("Recommend"):
    recommendations, posters = recommend(selectedMovieName)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
