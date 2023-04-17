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
sys.path.append('./config/')
from config import *
import streamlit as st
st.set_page_config(page_title='WIDE - Song Features Search', page_icon=':bar_chart:', layout="wide", initial_sidebar_state="auto", menu_items=None)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                           client_secret= client_secret))

df = pd.read_csv('../data/biggest.csv')

st.image('../src/img/logo.png', width=650)
st.divider()
def search_song(title, artist):
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


def user_select(results):
    #st.write(results)
    base_url = 'https://open.spotify.com/track/'
    counter = 1
    index = 0
    songs = []
    counter_lst = ['1','2','3','4','5']
    artists_lst = []
    artists_id = []
    album_lst = []
    title_lst = []
    link_lst = []
    selection_lst = []
    pics_lst = []
    for i in range(1, len(results['tracks']['items'])+1):
        title_lst.append(results['tracks']['items'][index]['name'])
        album_lst.append(results['tracks']['items'][index]['album']['name'])
        artists_lst.append(results['tracks']['items'][index]['artists'][0]['name'])
        artists_id.append(results['tracks']['items'][index]['artists'][0]['id'])
        link_lst.append(base_url+results['tracks']['items'][index]['id'])
        songs.append(results['tracks']['items'][index]['id'])
        selection = str(counter)+' - '+title_lst[index]+' - '+album_lst[index]+' by '+artists_lst[index]
        selection_lst.append(selection)
        pics_lst.append(results['tracks']['items'][index]['album']['images'][1]['url'])
        counter += 1
        index += 1

    user_select_df = pd.DataFrame(counter_lst)
    user_select_df.rename(columns={0: 'No.'}, inplace=True)
    user_select_df['Song Title'] = title_lst
    user_select_df['Album'] = album_lst
    user_select_df['Artist'] = artists_lst
    user_select_df['URL'] = link_lst
    user_select_df['URL'] = user_select_df['URL'].apply(make_clickable)
    st.write(HTML(user_select_df.to_html(index=False,escape=False)))
    st.subheader('')

    user_selection = st.radio('Please select a song from the below options (song - album - artist)', (selection_lst[0], selection_lst[1], selection_lst[2], selection_lst[3], selection_lst[4]))
    if user_selection == selection_lst[0]:
        st.image(pics_lst[0], width=300)
        return songs[0]
    elif user_selection == selection_lst[1]:
        st.image(pics_lst[1], width=300)
        return songs[1]
    elif user_selection == selection_lst[2]:
        st.image(pics_lst[2], width=300)
        return songs[2]
    elif user_selection == selection_lst[3]:
        st.image(pics_lst[3], width=300)
        return songs[3]
    elif user_selection == selection_lst[4]:
        st.image(pics_lst[4], width=300)
        return songs[4]
    else:
        st.write('Please select one song')

def get_audio_features(song_id):
    los=[]
    try:
        x = sp.audio_features(song_id)[0]
        if x: los.append(x)
    except:
        pass
    df = pd.DataFrame(los)
    df = df[['danceability', 'energy', 'key', 'loudness',
             'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
             'valence', 'tempo']]
    return df


def scaler(df):
    X = df.copy()
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns = X.columns)
    return X_scaled_df

def clustering(X_scaled_df, tempo_weight):
    kmeans = KMeans(n_clusters=8, random_state=1234)
    kmeans.fit(X_scaled_df, tempo_weight)
    clusters = kmeans.predict(X_scaled_df)
    pd.Series(clusters).value_counts().sort_index()
    X_scaled_df["cluster"] = clusters
    track_cluster = X_scaled_df.iloc[-1]
    final = track_cluster['cluster']
    return final

def make_clickable(link):
    return '<a href="{0}">{0}</a>'.format(link)

def selector(final_scaled, database, song_id, final, df2, selection, title, artist):

    song_recomender_df = pd.concat([database[['title','artist','id','source']],final_scaled],axis=1)
    song_recomender_df_hot = song_recomender_df[(song_recomender_df['source'] == 'H')]
    song_recomender_df_nonhot = song_recomender_df[(song_recomender_df['source'] == 'N')]

    if song_id in song_recomender_df_hot:
        song_recomender_test = song_recomender_df_hot[(song_recomender_df_hot['cluster'] == final)].sample(selection)
    else:
        song_recomender_test = song_recomender_df_nonhot[(song_recomender_df_nonhot['cluster'] == final)].sample(selection)

    song_recomender_test = song_recomender_test[['title','artist', 'id']]
    base_url = 'https://open.spotify.com/track/'
    id_list = list(song_recomender_test['id'])
    url_list = [base_url + i for i in id_list]
    song_recomender_test['url'] = url_list
    song_recomender_test['url'] = song_recomender_test['url'].apply(make_clickable)


    song_recomender_test = song_recomender_test.drop(['id'], axis=1)
    song_recomender_test.rename(columns={'title':'Song Title', 'artist':'Artist Name', 'url':'URL'}, inplace=True)
    st.write('Displaying', selection, 'similar song(s) to your selection: \n')
    st.write(HTML(song_recomender_test.to_html(index=False,escape=False)))


    #Graph
    st.divider()
    st.title(':violet[Song Features visualization]')
    with st.container():
        df2 = df2[['danceability','energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
        'valence']]

        categories=list(df2)[0:]
        N = len(categories)

        values = df2.loc[0].values.flatten().tolist()
        values += values[:1]
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]


        ax = plt.subplot(111, projection='polar')

        plt.rcParams['figure.facecolor'] = 'black'
        plt.xticks(angles[:-1], categories, color='grey', size=8)


        ax.set_rlabel_position(0)
        plt.yticks([0.20,0.40,0.60,0.8], ['0.20','0.40','0.60','0.8'], color="grey", size=7)
        plt.ylim(0,1)

        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle='solid', color = 'm')

        # Fill area
        ax.fill(angles, values, 'm', alpha=0.1)

        # Show the graph
        print('These are the features of the song you like!\n')
        plt.tight_layout()
        plt.show()
        st.pyplot(use_container_width=False)

def song_recommender(df, title, artist):
    #Get song id
    database = df
    results = search_song(title, artist)

    #Make user select
    song_id = user_select(results)

    #Get audio features of the song and display them
    df2 = get_audio_features(song_id)
    tempo = df2['tempo']
    tempo = tempo[0]
    tempo_up = tempo + 10
    tempo_weight = np.arange(tempo, tempo_up, 2)

    #Scale song feat by adding it to our database and then returning it scaled.
    df3 = database[['danceability', 'energy', 'key', 'loudness',
                    'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                    'valence', 'tempo']]
    df4 = pd.concat([df3,df2],axis=0)
    df_scaled = scaler(df4)
    final = clustering(df_scaled, tempo_weight)

    final_scaled = df_scaled.iloc[0:-1]
    st.divider()
    try:
        selection = st.slider('\nHow many songs do you want us to recommend you? Maximum 20!\n', min_value=1, max_value=20, value=5)
    except:
        print('\nInvalid value.\n')
        selection = 5
    title = title.title()
    artist = artist.title()
    selector(final_scaled, database, song_id, final, df2, selection, title, artist)
    st.subheader(':violet[Features explanation]')
    st.caption('Scale: from 0 to 1')
    st.write(':violet[Energy:] Represents how intense and active the song is.')
    st.write(':violet[Danceability:] Describes how suitable a track is for dancing.')
    st.write(':violet[Valence:] Measures the musical positiveness. The higher, the more cheerful.')
    st.write(':violet[Liveness:] Detects if the track was recorded live.')
    st.write(':violet[Instrumentalness:] Indicates if the rack contains no vocals.')
    st.write(':violet[Acousticness:] Shows the possibility of the track being acoustic.')
    st.write(':violet[Speechiness:] Detects the presence of spoken words in a track.')

title_input_container = st.empty()
title = title_input_container.text_input("Please enter song name: ")

if title != "":
    title_input_container.empty()
    st.info(title)

artist_input_container = st.empty()
artist = artist_input_container.text_input("Please enter artist name: ")

if artist != "":
    artist_input_container.empty()
    st.info(artist)


if title and artist:
    title = title.title()
    artist = artist.title()
    st.write(':violet[Your seach:]', title, ':violet[by]', artist)
    st.divider()
    st.title(':violet[Search results:]')
    title = title.lower()
    artist = artist.lower()
    song_recommender(df, title, artist)
