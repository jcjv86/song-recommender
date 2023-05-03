import pandas as pd
import sys
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
from Recommender import *
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
import webbrowser
import random
st.set_page_config(page_title='WIDE - Related Artist Search', page_icon=':singer:', layout="wide", initial_sidebar_state="auto", menu_items=None)

from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private user-top-read user-follow-read"))


st.image('../src/img/logo.png', width=650)
st.title('')
st.caption(':violet[*Take a walk on the WIDE side*]')
st.divider()

def make_clickable(link):
    return '<a href="{0}">{0}</a>'.format(link)

title = st.text_input("Please enter song name: ")
artist = st.text_input("Please enter artist name: ")

wide = Recommender()
if title and artist:
    st.write(':violet[Your search:]', title.title(), ':violet[by]', artist.title())
    # //// First search after user input ////
    results = wide.search_song(title, artist)
    st.divider()
    if results:
        # //// Second search: artist details ////
        artist_id = wide.user_select(results)
        if artist_id:
            # //// Control flow: button. Prevents making API call on each dataframe click. ////
            st.subheader(':violet[Is this your song?]')
            st.header('')
            ra_searcher = st.button('Yes! Show me the related artists, please.')
            st.header('')
            playlist = st.checkbox('Click me to also generate a playlist with the related artists songs', value=False)
            st.divider()
            if ra_searcher:
                st.title(':violet[Related artists:]')
                st.title('')
                # //// Third search: related artists ////
                related_artists_name, related_artists_url, related_artists_pic, related_artists_id = wide.related_artists(artist_id)
                if related_artists_id:
                    wide.related_artists_display(related_artists_name, related_artists_url, related_artists_pic)
                    st.divider()
                    if playlist:
                        with st.spinner('Please wait, getting songs...'):
                            ra_song_name, ra_artist_name, ra_album_name, ra_song_url, ra_song_uri = wide.related_artists_songs(related_artists_id)
                            data = {'Title': [i for i in ra_song_name],'Artist': [i for i in ra_artist_name],'URL' : [i for i in ra_song_url]}
                            df = pd.DataFrame(data)
                            df['URL'] = df['URL'].apply(make_clickable)
                            st.title(':violet[This is your song list:]')
                            st.title('')
                            st.write(HTML(df.to_html(index=False,escape=False)))
                            st.title('')
                            st.divider()
                            st.title('')
                            playlist_url=wide.playlist_generator(ra_song_uri, playlist_id)
                        st.success('Done! Enjoy your new music! New tab will be opened soon 🎶')
                        time.sleep(4)
                        webbrowser.open(playlist_url)
                else:
                    st.write('Sorry, no related artists found')
