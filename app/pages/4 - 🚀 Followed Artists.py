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
st.set_page_config(page_title='WIDE - User Followed Artists', page_icon=':rocket:', layout="wide", initial_sidebar_state="auto", menu_items=None)

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
st.title(':violet[Followed Artists]')
st.title('')
st.title('')
number_artists = st.slider('How many artists do you want to show?', min_value=1, max_value=1000, value=50)
st.caption('Search time increases by 2 seconds for every 50 artists block due to Spotify API limitations. Please be patient!')
time.sleep(1)

if number_artists < 51:
    following = (wide.user_following(number_artists))
    following = following['artists']['items']
    #st.write(following)
    artists_names = []
    artists_genres = []
    artists_ids = []
    artists_followers = []
    index=0
    for i in range(1, len(following)+1):
        artists_names.append(following[index]['name'])
        artists_genres.append(following[index]['genres'])
        artists_ids.append(following[index]['id'])
        artists_followers.append(following[index]['followers']['total'])
        index += 1

    df = {'Artist': [i for i in artists_names],
        'Genre': [i for i in artists_genres],
        'Followers': [i for i in artists_followers]
        }

    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)

elif (number_artists > 50):
    n = int(number_artists/50)
    rest = number_artists - n*50
    artists_names = []
    artists_genres = []
    artists_ids = []
    artists_followers = []
    following = (wide.user_following(50))
    following = following['artists']['items']
    index=0
    for i in range(1, len(following)+1):
        artists_names.append(following[index]['name'])
        artists_genres.append(following[index]['genres'])
        artists_ids.append(following[index]['id'])
        artists_followers.append(following[index]['followers']['total'])
        index += 1
    time.sleep(2)
    number_artists -= 50
    x=1
    while number_artists > 49 :
        for i in range(2, n+1):
            following[x] = (wide.user_following(50, after=artists_ids[-1]))
            following[x] = following[x]['artists']['items']
            index=0
            for i in range(1, len(following[x])+1):
                artists_names.append(following[x][index]['name'])
                artists_genres.append(following[x][index]['genres'])
                artists_ids.append(following[x][index]['id'])
                artists_followers.append(following[x][index]['followers']['total'])
                index += 1
            x += 1
            time.sleep(2)
            number_artists -= 50
    else:
        if rest > 0 :
            following_rest = wide.user_following((rest), after=artists_ids[-1])
            following_rest = following_rest['artists']['items']
            index=0
            for i in range(1, len(following_rest)+1):
                artists_names.append(following_rest[index]['name'])
                artists_genres.append(following_rest[index]['genres'])
                artists_ids.append(following_rest[index]['id'])
                artists_followers.append(following_rest[index]['followers']['total'])
                index += 1

    df = {'Artist': [i for i in artists_names],
        'Genre': [i for i in artists_genres],
        'Followers': [i for i in artists_followers]
        }
    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)
st.write('Displaying ' +str(len(data)) + ' artist(s)')

import plotly.express as px

fig = px.scatter(x=data["Followers"],
	         size=data["Followers"], color=data["Artist"], hover_name=data["Artist"],
	         labels={'x': 'Followers', 'y': 'Position', 'color':'Artist', 'size':'Followers'},
                 title='Artists by number of Followers', log_x=True, size_max=60)
fig.update_layout(height=1000)
fig.update_traces(textfont_size=10, cliponaxis=False)

st.plotly_chart(fig, use_container_width=True, height=1000)
