import pandas as pd
import sys
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter('ignore')
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from math import pi
import time
from IPython.display import HTML
sys.path.append('./config/')
sys.path.append('./lib')
from config import client_id
from config import client_secret
from config import playlist_id
from Stats import *
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
import webbrowser
import random
st.set_page_config(page_title='WIDE - Related Artist Search', page_icon=':singer:', layout="wide", initial_sidebar_state="auto", menu_items=None)

from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private user-top-read user-follow-read user-read-recently-played"))

st.image('../src/img/logo.png', width=650)
st.title('')
st.caption(':violet[*Take a walk on the WIDE side*]')
st.divider()
wide = Stats()
st.title(':violet[Recently played by user]')
st.title('')
st.title('')
number_songs = st.slider('How many recently played tracks do you want to show?', min_value=1, max_value=50, value=50)
#st.caption('Search time increases by 2 seconds for every 50 songs block due to Spotify API limitations. Please be patient!')
time.sleep(1)

if number_songs < 51:
    recent = (wide.recently_played(number_songs))
    recent = recent['items']
    artists_names = []
    songs_titles = []
    songs_albums = []
    albums_release = []
    last_played = []
    song_ids=[]
    index=0
    for i in range(1, len(recent)+1):
        artists_names.append(recent[index]['track']['artists'][0]['name'])
        song_ids.append(recent[index]['track']['id'])
        songs_titles.append(recent[index]['track']['name'])
        songs_albums.append(recent[index]['track']['album']['name'])
        albums_release.append(recent[index]['track']['album']['release_date'][0:4])
        last_played.append(recent[index]['played_at'][0:10] + ' - ' + recent[index]['played_at'][11:19])
        index += 1

    df = {'Song Title': [i for i in songs_titles],
          'Artist': [i for i in artists_names],
          'Album': [i for i in songs_albums],
          'Release date': [i for i in albums_release],
          'Last Played (date - hour)': [i for i in last_played]
        }

    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)

elif (number_songs > 50):
    n = int(number_songs/50)
    rest = number_songs - n*50
    artists_names = []
    songs_titles = []
    songs_albums = []
    albums_release = []
    last_played = []
    song_ids=[]
    recent = (wide.recently_played(50))
    cursor = recent['cursors']['before']
    recent = recent['items']
    index=0
    for i in range(1, len(recent)+1):
        artists_names.append(recent[index]['track']['artists'][0]['name'])
        song_ids.append(recent[index]['track']['id'])
        songs_titles.append(recent[index]['track']['name'])
        songs_albums.append(recent[index]['track']['album']['name'])
        albums_release.append(recent[index]['track']['album']['release_date'][0:4])
        last_played.append(recent[index]['played_at'][0:10] + ' - ' + recent[index]['played_at'][11:19])
        index += 1
    time.sleep(2)
    number_songs -= 50

    while number_songs > 49 :
        for i in range(2, n+1):
            recent = wide.recently_played(50, after=cursor)
            cursor = recent['cursors']['before']
            recent = recent['items']
            index=0
            for i in range(1, len(recent)+1):
                artists_names.append(recent[index]['track']['artists'][0]['name'])
                song_ids.append(recent[index]['track']['id'])
                songs_titles.append(recent[index]['track']['name'])
                songs_albums.append(recent[index]['track']['album']['name'])
                albums_release.append(recent[index]['track']['album']['release_date'][0:4])
                last_played.append(recent[index]['played_at'][0:10] + ' - ' + recent[index]['played_at'][11:19])
                index += 1

            time.sleep(2)
            number_songs -= 50
    else:
        if rest > 0 :
            recent_rest = wide.recently_played(rest, after=cursor)
            recent_rest = recent_rest['items']
            index=0
            for i in range(1, len(recent_rest)+1):
                artists_names.append(recent_rest[index]['track']['artists'][0]['name'])
                song_ids.append(recent_rest[index]['track']['id'])
                songs_titles.append(recent_rest[index]['track']['name'])
                songs_albums.append(recent_rest[index]['track']['album']['name'])
                albums_release.append(recent_rest[index]['track']['album']['release_date'][0:4])
                last_played.append(recent_rest[index]['played_at'][0:10] + ' - ' + recent_rest[index]['played_at'][11:19])
                index += 1

    df = {'Song Title': [i for i in songs_titles],
          'Artist': [i for i in artists_names],
          'Album': [i for i in songs_albums],
          'Release date': [i for i in albums_release],
          'Last Played (date - hour)': [i for i in last_played]
        }
    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)
st.write('Displaying last ' +str(len(data)) + ' played song(s).')
st.title('')
st.title('')
st.caption(':red[Note: It appears that there is currently an issue with this method - some songs are not displayed or updated unless user listens to them for at least a specific time, also the cursors are not working properly, blocking the data that can be accessed in the last 50 songs.]\n\n:red[Sorry for the inconvenience!]')
