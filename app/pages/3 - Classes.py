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
from spotipy.oauth2 import SpotifyClientCredentials
from IPython.display import HTML
import matplotlib.pyplot as plt
from math import pi
import time
sys.path.append('./config/')
from config import *
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
import webbrowser
import random
st.set_page_config(page_title='WIDE - Related Artist Search', page_icon=':singer:', layout="wide", initial_sidebar_state="auto", menu_items=None)

from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private"))


st.image('../src/img/logo.png', width=650)

playlist_items_search = sp.playlist_items(playlist_id)
playlist_items = []
index=0
for i in range(1, len(playlist_items_search['items'])+1):
    playlist_items.append(playlist_items_search['items'][index]['track']['id'])
    index += 1

class Recommender():
    def __init__(self):
        self.title = title
        self.artist = artist
        '''
        self.results = results
        self.user_selection = user_selection
        self.artist_id = artist_id
        self.ra_song_uri = ra_song_uri
        '''

    def search_song(self, title, artist):
        title = title.lower()
        artist = artist.lower()
        try:
            results = sp.search(q=title+','+artist, limit=5)
        except:
            return 'na'
        while len(results['tracks']['items'])<5:
            title = str(input('Sorry not found. Please enter song title again: \n\n')).lower()
            artist = str(input('\nPlease enter artist name: \n\n')).lower()
            try:
                results = sp.search(q=title+','+artist, limit=5)
            except:
                return 'na'
        return results

    def user_select(self, results):
        def make_clickable(link):
            return '<a href="{0}">{0}</a>'.format(link)
        #st.write(results)
        base_url = 'https://open.spotify.com/track/'
        counter = 1
        index = 0
        songs = []
        artist_lst = []
        artist_id = []
        album_lst = []
        title_lst = []
        link_lst = []
        selection_lst = []
        pics_lst = []
        for i in range(1, len(results['tracks']['items'])+1):
            title_lst.append(results['tracks']['items'][index]['name'])
            album_lst.append(results['tracks']['items'][index]['album']['name'])
            artist_lst.append(results['tracks']['items'][index]['artists'][0]['name'])
            artist_id.append(results['tracks']['items'][index]['artists'][0]['id'])
            link_lst.append(base_url+results['tracks']['items'][index]['id'])
            songs.append(results['tracks']['items'][index]['id'])
            selection = str(counter)+'  ||  '+title_lst[index]+'  ||  '+album_lst[index]+' ||  '+artist_lst[index]
            selection_lst.append(selection)
            pics_lst.append(results['tracks']['items'][index]['album']['images'][1]['url'])
            counter += 1
            index += 1

        data = {
        'Title': [i for i in title_lst],
        'Album': [i for i in album_lst],
        'Artist': [i for i in artist_lst],
        'artist_id': [i for i in artist_id],
        'pics_lst': [i for i in pics_lst]
        }
        df = pd.DataFrame(data)

        # select the columns you want the users to see
        gb = GridOptionsBuilder.from_dataframe(df[["Title", "Album", "Artist"]])
        # configure selection
        gb.configure_selection(selection_mode="single", use_checkbox=True,
                               suppressRowDeselection=True, pre_selected_rows=[1])
        gb.configure_side_bar()
        gridOptions = gb.build()

        data = AgGrid(df,
              gridOptions=gridOptions,
              enable_enterprise_modules=True,
              allow_unsafe_jscode=True,
              update_mode=GridUpdateMode.SELECTION_CHANGED,
              columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)

        selected_rows = data["selected_rows"]
        if len(selected_rows) != 0:
            st.image(selected_rows[0]['pics_lst'])
            return(selected_rows[0]['artist_id'])
        else:
            st.write('Please select one option')


    def related_artists(self, artist_id):
        related_artists_id = []
        related_artists_name = []
        related_artists_pic = []
        related_artists_url = []
        songs_search = []
        index = 0
        related = sp.artist_related_artists(artist_id)
        if len(related)>0:
            for i in range(1, len(related)+1):
                related_artists_id.append(related['artists'][index]['id'])
                related_artists_url.append(related['artists'][index]['external_urls']['spotify'])
                related_artists_name.append(related['artists'][index]['name'])
                related_artists_pic.append(related['artists'][index]['images'][2]['url'])
                index += 1
            return related_artists_id
        else:
            pass

    def related_artists_songs(self, related_artists_id):
        ra_song_id = []
        ra_song_name = []
        ra_song_url = []
        ra_artist_name = []
        ra_album_name = []
        index=0
        for i in range(1, len(related_artists_id)+1):
            songs_search = sp.artist_top_tracks(related_artists_id[index])
            choice = random.randint(0,len(songs_search)-1)
            ra_song_id.append(songs_search['tracks'][choice]['id'])
            ra_song_name.append(songs_search['tracks'][choice]['name'])
            ra_song_url.append(songs_search['tracks'][choice]['external_urls']['spotify'])
            ra_album_name.append(songs_search['tracks'][choice]['album']['name'])
            ra_artist_name.append(songs_search['tracks'][choice]['artists'][0]['name'])
            index += 1
        ra_song_uri = []
        index=0
        for i in range(1, len(ra_song_id)+1):
            ra_tracks = sp.track(track_id = ra_song_id[index])
            ra_song_uri.append(ra_tracks['uri'])
            index += 1
        return ra_song_url


    def button_playlist(self):
        button_playlist = st.button('Click to add tracks to playlist and open in browser - see selected songs below :headphones:')
        if button_playlist:
            sp.playlist_remove_all_occurrences_of_items(playlist_id, playlist_items)
            sp.playlist_add_items(playlist_id, items=ra_song_url)
            webbrowser.open(playlist_url)
#Class end

title = st.text_input("Please enter song name: ")
artist = st.text_input("Please enter artist name: ")

st.write(':violet[Your search:]', title.title(), ':violet[by]', artist.title())

wide = Recommender()
if title and artist:
    results = wide.search_song(title, artist)
    st.divider()
    if results:
        artist_id = wide.user_select(results)
        if artist_id:
            related_artists_id = wide.related_artists(artist_id)
            if related_artists_id:
                ra_song_url = wide.related_artists_songs(related_artists_id)
                wide.button_playlist()
            else:
                st.write('Sorry, not enough related artists found')
