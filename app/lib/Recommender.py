import pandas as pd
import warnings
warnings.simplefilter('ignore')
import time
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode, DataReturnMode
import webbrowser
import random
import sys
from IPython.display import HTML
sys.path.append('../config/')
import spotipy
import spotipy as sp
from config import client_id
from config import client_secret
from config import playlist_id
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private"))


class Recommender():
    def __init__(self):
        
        '''
        self.results = results
        self.user_selection = user_selection
        self.artist_id = artist_id
        self.ra_song_uri = ra_song_uri
        '''


    #  ||||    First API call - 1 search    ||||

    def search_song(self, title, artist):
        title = title.lower()
        artist = artist.lower()
        try:
            results = sp.search(q=title+','+artist, limit=5)
        except:
            return 'na'
        return results

    def user_select(self, results):
        '''
        Extracts the initial search info and builds a dataframe with 
        Title, Artist, Album and Year to allow user to select song.
        '''
        #st.write(results)
        base_url = 'https://open.spotify.com/track/'
        counter = 1
        index = 0
        songs = []
        artist_lst = []
        artist_id = []
        album_lst = []
        release_year = []
        album_url = []
        title_lst = []
        link_lst = []
        pics_lst = []
        for i in range(1, len(results['tracks']['items'])+1):
            title_lst.append(results['tracks']['items'][index]['name'])
            album_lst.append(results['tracks']['items'][index]['album']['name'])
            release_year.append(results['tracks']['items'][index]['album']['release_date'][0:4])
            album_url.append(results['tracks']['items'][index]['album']['external_urls']['spotify'])
            artist_lst.append(results['tracks']['items'][index]['artists'][0]['name'])
            artist_id.append(results['tracks']['items'][index]['artists'][0]['id'])
            link_lst.append(base_url+results['tracks']['items'][index]['id'])
            songs.append(results['tracks']['items'][index]['id'])
            pics_lst.append(results['tracks']['items'][index]['album']['images'][1]['url'])
            counter += 1
            index += 1

        #Artist Selection Dataframe AG Grid
        data = {
        'Title': [i for i in title_lst],
        'Album': [i for i in album_lst],
        'Artist': [i for i in artist_lst],
        'Album Release Year': [i for i in release_year],
        'URL' : [i for i in album_url],
        'artist_id': [i for i in artist_id],
        'pics_lst': [i for i in pics_lst]
        }
        df = pd.DataFrame(data)

        # select visible columns
        gb = GridOptionsBuilder.from_dataframe(df[["Title", "Album", "Artist", 'Album Release Year']])
        # configure selection
        gb.configure_selection(selection_mode="single", use_checkbox=True,
                               suppressRowDeselection=True)
        gb.configure_default_column(resizable=False, filterable=False)
        gridOptions = gb.build()

        data = AgGrid(df,
              gridOptions=gridOptions,
              fit_columns_on_grid_load=True,
              allow_unsafe_jscode=False,
              update_mode=GridUpdateMode.SELECTION_CHANGED,
              theme='streamlit',
              columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        
        selected_rows = data["selected_rows"]
        if len(selected_rows) != 0:
            st.image(selected_rows[0]['pics_lst'])
            return(selected_rows[0]['artist_id'])
        else:
            st.write('Please select one option')


    # ||||    Second API call    ||||

    def related_artists(self, artist_id):
        related_artists_id = []
        related_artists_name = []
        related_artists_pic = []
        related_artists_url = []
        index = 0
        related = sp.artist_related_artists(artist_id)

        if len(related)>0:
            for i in range(1, len(related['artists'])+1):
                related_artists_id.append(related['artists'][index]['id'])
                related_artists_url.append(related['artists'][index]['external_urls']['spotify'])
                related_artists_name.append(related['artists'][index]['name'])
                related_artists_pic.append(related['artists'][index]['images'][2]['url'])
                index += 1
        else:
            return 0

        return related_artists_name, related_artists_url, related_artists_pic, related_artists_id

    def related_artists_display(self, related_artists_name, related_artists_url, related_artists_pic):
        x = len(related_artists_name)
        index = 0
        if x > 0:
            #If RA = 20, 15, 10, 5
            if x % 5 == 0:
                if x/5 == 4:
                    counter = 20
                elif x/5 == 3:
                    counter = 15
                elif x/5 == 2:
                    counter = 10
                elif x/5 == 1:
                    counter = 5
            #If RA = 16, 11, 6
            elif x % 5 == 1:
                if x/5 == 3.2:
                    counter = 16
                elif x/5 == 2.2:
                    counter = 11
                elif x/5 == 1.2:
                    counter = 6
                #If RA = 1
                elif x/5 == 0.2:
                    counter = 1
                    while counter > 0:
                        col1 = st.columns(1)
                        with col1:
                            button1 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button1:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
            #If RA = 17, 12, 7, 2
            elif x % 5 == 2:
                if x/5 == 3.4:
                    counter = 17
                elif x/5 == 2.4:
                    counter = 12
                elif x/5 == 1.4:
                    counter = 7
                #If RA = 2
                elif x/5 == 0.4:
                    counter = 2
                    while counter > 0:
                        col1, col2 = st.columns(2)
                        with col1:
                            button1 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button1:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
                        with col2:
                            button2 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button2:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
            #If RA = 18, 13, 8, 3
            elif x % 5 == 3:
                if x/5 == 3.6:
                    counter = 18
                elif x/5 == 2.6:
                    counter = 13
                elif x/5 == 1.6:
                    counter = 8
                #If RA = 3
                elif x/5 == 0.6:
                    counter = 3
                    while counter > 0:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            button1 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button1:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
                        with col2:
                            button2 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button2:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
                        with col3:
                            button3 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button3:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
            #If RA = 19, 14, 9, 4
            elif x % 5 == 4:
                if x/5 == 3.8:
                    counter = 19
                elif x/5 == 2.8:
                    counter = 14
                elif x/5 == 1.8:
                    counter = 9
                #If RA = 4
                elif x/5 == 0.8:
                    counter =4
                    while counter > 0:
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            button1 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button1:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
                        with col2:
                            button2 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button2:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
                        with col3:
                            button3 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button3:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
                        with col4:
                            button4 = st.button(related_artists_name[index])
                            st.image(related_artists_pic[index])
                            if button4:
                                webbrowser.open(related_artists_url[index])
                        index += 1
                        counter -= 1
            while counter > 4:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    button1 = st.button(related_artists_name[index])
                    st.image(related_artists_pic[index])
                    if button1:
                        webbrowser.open(related_artists_url[index])
                index += 1
                counter -= 1
                with col2:
                    button2 = st.button(related_artists_name[index])
                    st.image(related_artists_pic[index])
                    if button2:
                        webbrowser.open(related_artists_url[index])
                index += 1
                counter -= 1
                with col3:
                    button3 = st.button(related_artists_name[index])
                    st.image(related_artists_pic[index])
                    if button3:
                        webbrowser.open(related_artists_url[index])
                index += 1
                counter -= 1
                with col4:
                    button4 = st.button(related_artists_name[index])
                    st.image(related_artists_pic[index])
                    if button4:
                        webbrowser.open(related_artists_url[index])
                index += 1
                counter -= 1
                with col5:
                    button5 = st.button(related_artists_name[index])
                    st.image(related_artists_pic[index])
                    if button5:
                        webbrowser.open(related_artists_url[index])
                index += 1
                counter -= 1


    # ////    Fourth API call: CAUTION! Up to 20 Searches. 3 sec timer between calls    ////

    def related_artists_songs(self, related_artists_id):
        ra_song_id = []
        ra_song_name = []
        ra_song_url = []
        ra_artist_name = []
        ra_album_name = []
        ra_song_uri = []
        index=0
        for i in range(1, len(related_artists_id)+1):
            songs_search = sp.artist_top_tracks(related_artists_id[index])
            choice = random.randint(0,len(songs_search)-1)
            ra_song_id.append(songs_search['tracks'][choice]['id'])
            ra_song_name.append(songs_search['tracks'][choice]['name'])
            ra_song_url.append(songs_search['tracks'][choice]['external_urls']['spotify'])
            ra_album_name.append(songs_search['tracks'][choice]['album']['name'])
            ra_artist_name.append(songs_search['tracks'][choice]['artists'][0]['name'])
            ra_song_uri.append(songs_search['tracks'][choice]['uri'])
            time.sleep(3)
            index += 1
        return ra_song_name, ra_artist_name, ra_album_name, ra_song_url, ra_song_uri

        

    def button_playlist(self, ra_song_uri, playlist_id):
        #playlist_id imported from config file.
        playlist_url = 'https://open.spotify.com/playlist/' + playlist_id
        playlist_items_search = sp.playlist_items(playlist_id)
        playlist_items = []
        index=0
        for i in range(1, len(playlist_items_search['items'])+1):
            playlist_items.append(playlist_items_search['items'][index]['track']['id'])
            index += 1
            time.sleep(3)
        sp.playlist_remove_all_occurrences_of_items(playlist_id, playlist_items)
        sp.playlist_add_items(playlist_id, items=ra_song_uri)
        webbrowser.open(playlist_url)
