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
st.title(':violet[User info]')
st.title('')
st.title('')
user = wide.user_info()
st.subheader(':violet[Name:] ' + user['display_name'])

st.subheader(':violet[Alias:] ' + user['id'])

st.subheader(':violet[Your profile pic:]')
st.image((user['images'][0]['url']), width=200)

st.subheader(':violet[Link to profile:] ' + user['external_urls']['spotify'])

st.subheader(':violet[User Followers:] ' + 'You have ' + str(user['followers']['total']) + ' followers')
st.divider()



'''
time.sleep(timer)
st.write('User top artists')
st.write(wide.top_artists())
time.sleep(timer)
st.write('User top tracks')
st.write(wide.top_tracks(time_range='long_term'))
'''
