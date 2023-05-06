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
st.title(':violet[Top Tracks]')
st.title('')
st.title('')
number_songs = st.slider('Up to how many artists do you want to show?', min_value=1, max_value=50, value=50)
#st.caption('Search time increases by 2 seconds for every 50 artists block due to Spotify API limitations. Please be patient!')
time.sleep(1)
st.title('')
time_select = st.radio('Set your time frame for the affinity calculation:', ('Last 4 weeks', 'Last 6 months', 'All time'))
if time_select == 'Last 4 weeks':
    time_range = 'short_term'
elif time_select == 'Last 6 months':
    time_range = 'medium_term'
else:
    time_range = 'long_term'

st.caption('This defines over what time frame the affinities are computed. Either your recently listened to artists or your all time favorite ones.')

st.divider()

if number_songs < 51:
    following = (wide.top_tracks(number_songs, time_range=time_range))
    following = following['items']
    #st.write(following)
    artists_names = []
    songs_titles = []
    songs_albums = []
    albums_release = []
    albums_pic = []
    albums_url=[]
    song_ids = []
    index=0
    for i in range(1, len(following)+1):
        artists_names.append(following[index]['artists'][0]['name'])
        songs_titles.append(following[index]['name'])
        songs_albums.append(following[index]['album']['name'])
        albums_release.append(following[index]['album']['release_date'][0:4])
        albums_pic.append(following[index]['album']['images'][1]['url'])
        albums_url.append(following[index]['album']['external_urls']['spotify'])
        song_ids.append(following[index]['id'])
        index += 1

    df = {'Song Title': [i for i in songs_titles],
          'Artist': [i for i in artists_names],
          'Album': [i for i in songs_albums],
          'Release date': [i for i in albums_release]
        }

    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)

#As with Recently played module, Spotify API has some limitations that set the maximum number of artists recoverable on 50. In case these limitations were lifted, the following code would get the extra info. Just set the max_value in line 39 as desired.
elif (number_songs > 50):
    n = int(number_songs/50)
    rest = number_songs - n*50
    artists_names = []
    songs_titles = []
    songs_albums = []
    albums_release = []
    albums_pic = []
    albums_url=[]
    song_ids = []
    following = (wide.top_tracks(50, time_range='long_term'))
    following = following['items']
    index=0
    for i in range(1, len(following)+1):
        artists_names.append(following[index]['artists'][0]['name'])
        songs_titles.append(following[index]['name'])
        songs_albums.append(following[index]['album']['name'])
        albums_release.append(following[index]['album']['release_date'][0:4])
        albums_pic.append(following[index]['album']['images'][1]['url'])
        albums_url.append(following[index]['album']['external_urls']['spotify'])
        song_ids.append(following[index]['id'])
        index += 1
    time.sleep(2)
    number_songs -= 50
    x = 1
    while number_songs > 49 :
        for i in range(2, n+1):
            following[x] = wide.top_tracks(50, offset=(x*50), time_range='long_term')
            following[x] = following[x]['items']
            st.write(following[x])
            index=0
            for i in range(1, len(following[x])+1):
                artists_names.append(following[index]['artists'][0]['name'])
                songs_titles.append(following[index]['name'])
                songs_albums.append(following[index]['album']['name'])
                albums_release.append(following[index]['album']['release_date'][0:4])
                albums_pic.append(following[index]['album']['images'][1]['url'])
                albums_url.append(following[index]['album']['external_urls']['spotify'])
                song_ids.append(following[index]['id'])
                index += 1
            x += 1
            time.sleep(2)
            number_songs -= 50
    else:
        if rest > 0 :
            following_rest = wide.top_tracks(rest, offset=rest, time_range='long_term')
            following_rest = following_rest['items']
            index=0
            for i in range(1, len(following_rest)+1):
                artists_names.append(following[index]['artists'][0]['name'])
                songs_titles.append(following[index]['name'])
                songs_albums.append(following[index]['album']['name'])
                albums_release.append(following[index]['album']['release_date'][0:4])
                albums_pic.append(following[index]['album']['images'][1]['url'])
                albums_url.append(following[index]['album']['external_urls']['spotify'])
                song_ids.append(following[index]['id'])
                index += 1

    df = {'Song Title': [i for i in songs_titles],
          'Artist': [i for i in artists_names],
          'Album': [i for i in songs_albums],
          'Release date': [i for i in albums_release]
        }

    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)

st.write('Displaying ' +str(len(data)) + ' song(s)')

import plotly.express as px
df = data
position = [i for i in range(1,len(df)+1)]
df['Position'] = position
fig = px.bar(df, x='Position', y='Artist', color="Album", text='Song Title', title=(time_select+' favorite songs selection'))
fig.update_layout(height=1000)
fig.update_traces(textfont_size=10, cliponaxis=False)
st.plotly_chart(fig, use_container_width=True, height=1000)
st.divider()

#Top 10 artists display
if number_songs > 9:
    time_frame = time_select+' favorite songs selection'
    st.title(':violet[Your Top 10 Songs] - '+time_frame)
    st.title('')
    st.title('')
    st.title('')
    st.subheader(':violet[**Top 3**]')
    st.subheader('')
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.subheader(':violet[# 1]')
        st.subheader(songs_titles[0])
        st.subheader('')
        st.write('by '+artists_names[0])
        button_a = st.button(songs_albums[0])
        st.subheader('')
        st.image(albums_pic[0])
        if button_a:
            webbrowser.open(albums_url[0])
    with col_b:
        st.subheader(':violet[# 2]')
        st.subheader(songs_titles[1])
        st.subheader('')
        st.write('by '+artists_names[1])
        button_b = st.button(songs_albums[1])
        st.subheader('')
        st.image(albums_pic[1])
        if button_b:
            webbrowser.open(albums_url[1])
    with col_c:
        st.subheader(':violet[# 3]')
        st.subheader(songs_titles[2])
        st.subheader('')
        st.write('by '+artists_names[2])
        button_c = st.button(songs_albums[2])
        st.subheader('')
        st.image(albums_pic[2])
        if button_c:
            webbrowser.open(albums_url[2])
    st.title('')
    st.title('')
    st.title('')
    st.subheader(':violet[The rest of your top 10]')
    st.subheader('')
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        st.subheader(':violet[# 4]')
        st.write(songs_titles[3])
        st.subheader('')
        st.write('by '+artists_names[3])
        button1 = st.button(songs_albums[3], key=1)
        st.subheader('')
        st.image(albums_pic[3])
        if button1:
            webbrowser.open(albums_url[3])
    with col2:
        st.subheader(':violet[# 5]')
        st.write(songs_titles[4])
        st.subheader('')
        st.write('by '+artists_names[4])
        button2 = st.button(songs_albums[4], key=2)
        st.subheader('')
        st.image(albums_pic[4])
        if button2:
            webbrowser.open(albums_url[4])
    with col3:
        st.subheader(':violet[# 6]')
        st.write(songs_titles[5])
        st.subheader('')
        st.write('by '+artists_names[5])
        button3 = st.button(songs_albums[5], key=3)
        st.subheader('')
        st.image(albums_pic[5])
        if button3:
            webbrowser.open(albums_url[5])
    with col4:
        st.subheader(':violet[# 7]')
        st.write(songs_titles[6])
        st.subheader('')
        st.write('by '+artists_names[6])
        button4 = st.button(songs_albums[6], key=4)
        st.subheader('')
        st.image(albums_pic[6])
        if button4:
            webbrowser.open(albums_url[6])
    with col5:
        st.subheader(':violet[# 8]')
        st.write(songs_titles[7])
        st.subheader('')
        st.write('by '+artists_names[7])
        button5 = st.button(songs_albums[7], key=5)
        st.subheader('')
        st.image(albums_pic[7])
        if button5:
            webbrowser.open(albums_url[7])
    with col6:
        st.subheader(':violet[# 9]')
        st.write(songs_titles[8])
        st.subheader('')
        st.write('by '+artists_names[8])
        button4 = st.button(songs_albums[8], key=6)
        st.subheader('')
        st.image(albums_pic[8])
        if button4:
            webbrowser.open(albums_url[8])
    with col7:
        st.subheader(':violet[# 10]')
        st.write(songs_titles[9])
        st.subheader('')
        st.write('by '+artists_names[9])
        button5 = st.button(songs_albums[9], key=7)
        st.subheader('')
        st.image(albums_pic[9])
        if button5:
            webbrowser.open(albums_url[9])
