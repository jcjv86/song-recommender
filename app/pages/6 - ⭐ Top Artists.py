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
st.set_page_config(page_title='WIDE - User Top Artists', page_icon=':top:', layout="wide", initial_sidebar_state="auto", menu_items=None)

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
st.title(':violet[Top Artists]')
st.title('')
st.title('')
number_artists = st.slider('Up to how many artists do you want to show?', min_value=1, max_value=50, value=50)
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

if number_artists < 51:
    following = (wide.top_artists(number_artists, time_range=time_range))
    following = following['items']
    #st.write(following)
    artists_names = []
    artists_genres = []
    artists_ids = []
    artists_url = []
    artists_pic = []
    index=0
    for i in range(1, len(following)+1):
        artists_names.append(following[index]['name'])
        artists_genres.append(following[index]['genres'])
        artists_ids.append(following[index]['id'])
        artists_url.append(following[index]['external_urls']['spotify'])
        artists_pic.append(following[index]['images'][1]['url'])
        index += 1

    df = {'Artist': [i for i in artists_names],
        'Genre': [i for i in artists_genres],
        'URL': [i for i in artists_url]
        }

    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)

#As with Recently played module, Spotify API has some limitations that set the maximum number of artists recoverable on 50. In case these limitations were lifted, the following code would get the extra info. Just set the max_value in line 39 as desired.
elif (number_artists > 50):
    n = int(number_artists/50)
    rest = number_artists - n*50
    artists_names = []
    artists_genres = []
    artists_ids = []
    artists_url = []
    artists_pic = []
    following = (wide.top_artists(50, time_range='long_term'))
    following = following['items']
    index=0
    for i in range(1, len(following)+1):
        artists_names.append(following[index]['name'])
        artists_genres.append(following[index]['genres'])
        artists_ids.append(following[index]['id'])
        artists_url.append(following[index]['external_urls']['spotify'])
        artists_pic.append(following[index]['images'][1]['url'])
        index += 1
    time.sleep(2)
    number_artists -= 50
    x = 1
    while number_artists > 49 :
        for i in range(2, n+1):
            following[x] = wide.top_artists(50, offset=(x*50), time_range='long_term')
            following[x] = following[x]['items']
            st.write(following[x])
            index=0
            for i in range(1, len(following[x])+1):
                artists_names.append(following[x][index]['name'])
                artists_genres.append(following[x][index]['genres'])
                artists_ids.append(following[x][index]['id'])
                artists_url.append(following[x][index]['external_urls']['spotify'])
                artists_pic.append(following[index]['images'][1]['url'])
                index += 1
            x += 1
            time.sleep(2)
            number_artists -= 50
    else:
        if rest > 0 :
            following_rest = wide.top_artists(rest, offset=rest, time_range='long_term')
            following_rest = following_rest['items']
            index=0
            for i in range(1, len(following_rest)+1):
                artists_names.append(following_rest[index]['name'])
                artists_genres.append(following_rest[index]['genres'])
                artists_ids.append(following_rest[index]['id'])
                artists_url.append(following_rest[index]['external_urls']['spotify'])
                artists_pic.append(following[index]['images'][1]['url'])
                index += 1

    df = {'Artist': [i for i in artists_names],
        'Genre': [i for i in artists_genres],
        'URL': [i for i in artists_url]
        }
    data = pd.DataFrame(df)
    st.dataframe(data, use_container_width=True)
st.write('Displaying ' +str(len(data)) + ' artist(s)')

import plotly.express as px
df = data
labels = [i for i in range(1,len(df)+1)]
df['Position'] = labels
fig = px.bar(df, x='Position', y='Artist', color="Artist", text='Genre', title=(time_select+' favorite artists selection'))
fig.update_layout(height=1000)
fig.update_traces(textfont_size=10, cliponaxis=False)
st.plotly_chart(fig, use_container_width=True, height=1000)
st.divider()

#Top 10 artists display
if number_artists > 9:
    time_frame = time_select+' favorite artists selection'
    st.title(':violet[Your Top 10 Artists] - '+time_frame)
    st.title('')
    st.title('')
    st.title('')
    st.subheader(':violet[**Top 3**]')
    st.subheader('')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(':violet[# 1]')
        button1 = st.button(artists_names[0])
        st.image(artists_pic[0])
        if button1:
            webbrowser.open(artists_url[0])
    with col2:
        st.subheader(':violet[# 2]')
        button2 = st.button(artists_names[1])
        st.image(artists_pic[1])
        if button2:
            webbrowser.open(artists_url[1])
    with col3:
        st.subheader(':violet[# 3]')
        button3 = st.button(artists_names[2])
        st.image(artists_pic[2])
        if button3:
            webbrowser.open(artists_url[2])
    st.title('')
    st.title('')
    st.title('')
    st.subheader(':violet[The rest of your top 10]')
    st.subheader('')
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1:
        button1 = st.button(artists_names[3])
        st.image(artists_pic[3])
        if button1:
            webbrowser.open(artists_url[3])
    with col2:
        button2 = st.button(artists_names[4])
        st.image(artists_pic[4])
        if button2:
            webbrowser.open(artists_url[4])
    with col3:
        button3 = st.button(artists_names[5])
        st.image(artists_pic[5])
        if button3:
            webbrowser.open(artists_url[5])
    with col4:
        button4 = st.button(artists_names[6])
        st.image(artists_pic[6])
        if button4:
            webbrowser.open(artists_url[6])
    with col5:
        button5 = st.button(artists_names[7])
        st.image(artists_pic[7])
        if button5:
            webbrowser.open(artists_url[7])
    with col6:
        button4 = st.button(artists_names[8])
        st.image(artists_pic[8])
        if button4:
            webbrowser.open(artists_url[8])
    with col7:
        button5 = st.button(artists_names[9])
        st.image(artists_pic[9])
        if button5:
            webbrowser.open(artists_url[9])
