#importing the necessary libraries
import streamlit as st
import pickle
import requests

#loading the movies dataset and the cosine similarity matrix
movies=pickle.load(open('movies.pkl','rb'))
cosine_similarity=pickle.load(open('similarity.pkl','rb'))

#fetching the movie posters
def fetch_posters(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=954d6d33447de185bc5f6826e186b159&language=en-US'.format(movie_id),timeout=10)
    data=response.json()
    poster_path=data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/original{poster_path}"
    else:
        st.warning("No poster found for this movie:",movie_id)
        return None
    

#fetching the recommended movie names
def recommendation(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=cosine_similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:7]
    recommended_movie=[]
    posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        if movie_id is None:
            st.warning("No movie found for title",)
        recommended_movie.append(movies.iloc[i[0]].title)
        posters.append(fetch_posters(movie_id))
    return recommended_movie,posters



st.title("Movie Recommendation System")
movie_list=movies['title'].values
selected_movie_name=st.selectbox("Choose or type the movie name",options=movie_list)

# recommend button
if st.button('Recommend'):
    recommended_movie,posters=recommendation(selected_movie_name)

# Displaying the poster and movie name
    if recommended_movie and posters:
        cols=st.columns(6)
        for col, movie, poster in zip(cols, recommended_movie, posters):
            with col:
                st.text(movie)
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.warning("Poster not avaiable")
    else:
        st.text("No recommendations found or posters unavailable.")

st.markdown(
    '''
    <style>
    .stApp {
        background: linear-gradient(56deg,#5072A7,#5F9EA0);
        }
    </style>
''',
    unsafe_allow_html=True
)
