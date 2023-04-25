import pandas as pd
import numpy as np
import sys
import os
import warnings
warnings.simplefilter('ignore')
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import spotipy
import json
from IPython.display import HTML
import matplotlib.pyplot as plt
from math import pi
sys.path.append('./config/')
sys.path.append('./lib')
from config import client_id
from config import client_secret
from config import playlist_id
from config import timer
from Features import *
import streamlit as st
import webbrowser
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode, DataReturnMode
st.set_page_config(page_title='WIDE - Song Features Search', page_icon=':bar_chart:', layout="wide", initial_sidebar_state="auto", menu_items=None)
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private"))

database = pd.read_csv('../data/biggest.csv')

st.image('../src/img/logo.png', width=650)
st.title('')
st.caption(':violet[*Take a walk on the WIDE side*]')
st.divider()

title = st.text_input("Please enter song name: ")
artist = st.text_input("Please enter artist name: ")


wide = Features()

if title and artist:
    #Song search
    results = wide.search_song(title, artist)
    #Song selection
    song_id = wide.user_select(results)
    if song_id:
        #Song features
        df_user_song = wide.get_audio_features(song_id)
        #Song tempo weight
        tempo = df_user_song['tempo']
        tempo = tempo[0]
        tempo_up = tempo + 10
        tempo_weight = np.arange(tempo, tempo_up, 2)
        #Song features df concat to database and scaled (so both database features and song are proportionally scaled)
        db = database[['danceability', 'energy', 'key', 'loudness',
                        'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']]
        combined_not_scaled_df = pd.concat([db, df_user_song], axis=0)
        combined_scaled_df = wide.scaler(combined_not_scaled_df)
        #Clustering, with tempo weight
        clustered_df = wide.clustering(combined_scaled_df, tempo_weight)
        #Selecting already scaled database without user song
        final_scaled = combined_scaled_df.iloc[0:-1]
        #User selection of number of songs to recommend
        st.divider()
        st.subheader(':violet[How many songs do you want us to recommend you? Maximum 20.]')
        #Final function to get recommended songs df and their ids and plot features graph.
        selection = st.slider('', min_value=1, max_value=20, value=5)
        selection_text = 'Show me ' + str(selection) + ' recommendations'
        st.caption(selection_text)
        st.divider()
        song_recomender_test, ax, recommended_songs_id = wide.selector(final_scaled, database, song_id, clustered_df, df_user_song, selection, title, artist)
        st.title(':violet[Displaying similar song(s) to your selection:]')
        st.write('')
        st.write(HTML(song_recomender_test.to_html(escape=False, index=False)))
        st.title('')
        st.divider()
        st.title(':violet[These are the main features of your song]')
        st.write('')
        st.pyplot(use_container_width=False)
        st.subheader(':violet[Features explained (*scale from 0 to 1*)]')
        #Song featues explanation arranged in 7 columns
        st.write('')
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

        with col1:
            st.write('**Energy**')
            st.caption('intense and active')
        with col2:
            st.write('**Danceability**')
            st.caption('suitable for dancing')
        with col3:
            st.write('**Valence**')
            st.caption('cheerful')
        with col4:
            st.write('**Liveness**')
            st.caption('recorded live')
        with col5:
            st.write('**Instrumentalness**')
            st.caption('no vocals')
        with col6:
            st.write('**Acousticness**')
            st.caption('acoustic')
        with col7:
            st.write('**Speechiness**')
            st.caption('spoken words')

        st.divider()
        playlist_gen = st.button('Generate playlist with recommendations')
        if playlist_gen:
            recommended_songs_id=list(recommended_songs_id)
            playlist_url = wide.playlist_generator(recommended_songs_id, playlist_id)
            st.success('Done! Enjoy your new music! New tab will be opened soon 🎶')
            time.sleep(5)
            webbrowser.open(playlist_url)
