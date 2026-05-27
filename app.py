import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🍿", layout="wide")

#HTML
st.markdown("""
<style>
    /* Style the recommend button */
    div.stButton > button:first-child {
        background-color: #E50914;
        color: white;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #B20710;
        transform: scale(1.02);
    }
    /* Center align the movie titles */
    .movie-title {
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
        font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]
    
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

#--------------------Frontend----------------------

st.title('🎬 Movie Recommendation System')
st.markdown("Discover your next favorite film based on what you already love.")

st.write("")

select_movie_name = st.selectbox(
    'Search for a movie:',
    movies['title'].values
)

if st.button('Recommend Movie'):
    with st.spinner('Curating recommendations for you...'):
        name, posters = recommend(select_movie_name)
    st.write("### Top Picks for You:")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0], use_container_width=True)
        st.markdown(f"<p class='movie-title'>{name[0]}</p>", unsafe_allow_html=True)
    with col2:
        st.image(posters[1], use_container_width=True)
        st.markdown(f"<p class='movie-title'>{name[1]}</p>", unsafe_allow_html=True)
    with col3:
        st.image(posters[2], use_container_width=True)
        st.markdown(f"<p class='movie-title'>{name[2]}</p>", unsafe_allow_html=True)
    with col4:
        st.image(posters[3], use_container_width=True)
        st.markdown(f"<p class='movie-title'>{name[3]}</p>", unsafe_allow_html=True)
    with col5:
        st.image(posters[4], use_container_width=True)
        st.markdown(f"<p class='movie-title'>{name[4]}</p>", unsafe_allow_html=True)