import pandas as pd
import numpy as np
import sys
import os
import warnings
warnings.simplefilter('ignore')
sys.path.append('../config/')
import time
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from config import *
#Timer can be configured in the config.py file
import spotipy
import json
from IPython.display import HTML
import matplotlib.pyplot as plt
from math import pi
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode, DataReturnMode
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private"))
def make_clickable(link):
        return '<a href="{0}">{0}</a>'.format(link)

class Features():

    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret

    #  ||||    First API call - 1 search    ||||
    # Makes a song title - song artist search, limit 5 songs.
    def search_song(self, title, artist):
        try:
            results = sp.search(q=title+','+artist, limit=5)
            return results
        except:
            return 'na'

    # Allows user to select the song among the 5 results with an streamlit AG Grid. Displays also the album art for easier recognition.
    def user_select(self, results):
        base_url = 'https://open.spotify.com/track/'
        index = 0
        songs_lst = []
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
            songs_lst.append(results['tracks']['items'][index]['id'])
            pics_lst.append(results['tracks']['items'][index]['album']['images'][1]['url'])
            index += 1

        # Artist Selection Dataframe AG Grid
        data = {
        'Title': [i for i in title_lst],
        'Album': [i for i in album_lst],
        'Artist': [i for i in artist_lst],
        'Album Release Year': [i for i in release_year],
        'URL' : [i for i in album_url],
        'song_id': [i for i in songs_lst],
        'pics_lst': [i for i in pics_lst]
        }
        df = pd.DataFrame(data)

        # select visible columns for the user
        gb = GridOptionsBuilder.from_dataframe(df[["Title", "Album", "Artist", 'Album Release Year']])
        # configure selection
        gb.configure_selection(selection_mode="single", use_checkbox=True,
                               suppressRowDeselection=True)
        gb.configure_default_column(resizable=False, filterable=False)
        gridOptions = gb.build()
        # build the dinamic dataframe
        data = AgGrid(df,
              gridOptions=gridOptions,
              fit_columns_on_grid_load=True,
              allow_unsafe_jscode=False,
              update_mode=GridUpdateMode.SELECTION_CHANGED,
              theme='streamlit',
              columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
        # What to do with selected dataframe rows
        selected_rows = data["selected_rows"]
        if len(selected_rows) != 0:
            st.image(selected_rows[0]['pics_lst'])
            return(selected_rows[0]['song_id'])
        else:
            st.write(':violet[Please select one option]')

    # ||||    Second API call    ||||
    # Song features search
    def get_audio_features(self, song_id):
        los=[]
        los.append(sp.audio_features(song_id)[0])
        df_user_song = pd.DataFrame(los)
        df_user_song = df_user_song[['danceability', 'energy', 'key', 'loudness',
                'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                'valence', 'tempo']]
        return df_user_song

    # Scaler function for the combined (User song + database) features dataframe (aka final dataframe)
    def scaler(self, combined_not_scaled_df):
        X = combined_not_scaled_df.copy()
        scaler = StandardScaler()
        scaler.fit(X)
        X_scaled = scaler.transform(X)
        combined_scaled_df = pd.DataFrame(X_scaled, columns = X.columns)
        return combined_scaled_df

    # Cluster function for the scaled final dataframe. Returns the searched song cluster no.
    def clustering(self, combined_scaled_df, tempo_weight):
        kmeans = KMeans(n_clusters=8, random_state=1234)
        kmeans.fit(combined_scaled_df, tempo_weight)
        clusters = kmeans.predict(combined_scaled_df)
        pd.Series(clusters).value_counts().sort_index()
        combined_scaled_df["cluster"] = clusters
        track_cluster = combined_scaled_df.iloc[-1]
        clustered_df = track_cluster['cluster']
        return clustered_df

    # Selector function: returns dataframe with recommendations from database based on song cluster. Returns also graph with song features.
    def selector(self, final_scaled, database, song_id, clustered_df, df_user_song, selection, title, artist):

        song_recomender_df = pd.concat([database[['title','artist','id','source']],final_scaled],axis=1)
        song_recomender_df_hot = song_recomender_df[(song_recomender_df['source'] == 'H')]
        song_recomender_df_nonhot = song_recomender_df[(song_recomender_df['source'] == 'N')]

        if song_id in song_recomender_df_hot:
            song_recomender_test = song_recomender_df_hot[(song_recomender_df_hot['cluster'] == clustered_df)].sample(selection)
        else:
            song_recomender_test = song_recomender_df_nonhot[(song_recomender_df_nonhot['cluster'] == clustered_df)].sample(selection)

        song_recomender_test = song_recomender_test[['title','artist', 'id']]
        base_url = 'https://open.spotify.com/track/'
        id_list = list(song_recomender_test['id'])
        url_list = [base_url + i for i in id_list]
        song_recomender_test['url'] = url_list
        song_recomender_test['url'] = song_recomender_test['url'].apply(make_clickable)

        recommended_songs_id = song_recomender_test['id']
        song_recomender_test = song_recomender_test.drop(['id'], axis=1)
        song_recomender_test.rename(columns={'title': 'Song Title', 'artist': 'Artist', 'url': 'URL'}, inplace=True)

        # //// Graph ////
        df_user_song = df_user_song[['danceability', 'energy', 'speechiness', 'acousticness',
                'instrumentalness', 'liveness', 'valence']]

        categories=list(df_user_song)[0:]
        N = len(categories)

        values = df_user_song.loc[0].values.flatten().tolist()
        values += values[:1]
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        ax = plt.subplot(111, projection='polar')

        plt.rcParams['figure.facecolor'] = 'black'
        plt.xticks(angles[:-1], categories, color='grey', size=8)

        ax.set_rlabel_position(0)
        plt.yticks([0.20,0.40,0.60,0.8], ['0.20','0.40','0.60','0.8'], color="grey", size=8)
        plt.ylim(0,1)

        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle='solid', color = 'm')

        # Fill area
        ax.fill(angles, values, 'm', alpha=0.1)

        return song_recomender_test, ax, recommended_songs_id

    # ////    Fifth API call: playlist items    ////
    # Playlist generator for the recommended songs. Since spotipy cannot empty the whole list without having the song IDs of the playlist, first we have to get this info from the playlist itself, then remove them and finally add all new songs. Makes the final call (Timer between them).
    def playlist_generator(self, recommended_songs_id, playlist_id):
        songs_uri = []
        base_uri = 'spotify:track:'
        index = 0
        for i in range(1, len(recommended_songs_id)+1):
            songs_uri.append(base_uri+recommended_songs_id[index])
            index += 1
        #playlist_id imported from config file.
        playlist_url = 'https://open.spotify.com/playlist/' + playlist_id
        playlist_items_search = sp.playlist_items(playlist_id)
        playlist_items = []
        index=0
        for i in range(1, len(playlist_items_search['items'])+1):
            playlist_items.append(playlist_items_search['items'][index]['track']['id'])
            index += 1
        sp.playlist_remove_all_occurrences_of_items(playlist_id, playlist_items)
        time.sleep(timer)
        sp.playlist_add_items(playlist_id, items=songs_uri)
        return(playlist_url)
