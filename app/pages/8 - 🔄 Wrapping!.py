import pandas as pd
import numpy as np
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
import plotly.express as px
st.set_page_config(page_title='WIDE - User Wrapping!', page_icon=':arrows_counterclockwise:', layout="wide", initial_sidebar_state="auto", menu_items=None)

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
st.title(':violet[Wrapping!]')
st.title('')
st.title('')
st.subheader('This is a summary of your user stats: **:violet[Followed artists]**, **:violet[Recently Played]**, **:violet[Top Artists]** and **:violet[Top Tracks]**.')
st.title('')
time_select = st.radio('Set your time frame for the affinity calculation:', ('Last 4 weeks', 'Last 6 months', 'All time'))
if time_select == 'Last 4 weeks':
    time_range = 'short_term'
elif time_select == 'Last 6 months':
    time_range = 'medium_term'
else:
    time_range = 'long_term'
st.title('')
number_artists = st.slider('How many of your followed artists do you want to show?', min_value=1, max_value=1000, value=50)
st.caption('Search time increases by 2 seconds for every 50 artists block due to Spotify API limitations. Please be patient!')
st.caption('''If you get less artists than the ones you requested it means that you don't follow that many. You will see displayed the number of total artists you follow.''')
fa_total=number_artists
number_songs = 50
st.divider()

#Followed Artists
if number_artists < 51:
    following = (wide.user_following(number_artists))
    following = following['artists']['items']
    #st.write(following)
    artists_names_fa = []
    artists_genres_fa = []
    artists_ids_fa = []
    artists_followers_fa = []
    index=0
    for i in range(1, len(following)+1):
        artists_names_fa.append(following[index]['name'])
        artists_genres_fa.append(following[index]['genres'])
        artists_ids_fa.append(following[index]['id'])
        artists_followers_fa.append(following[index]['followers']['total'])
        index += 1

    df = {'Artist': [i for i in artists_names_fa],
        'Genre': [i for i in artists_genres_fa],
        'Followers': [i for i in artists_followers_fa]
        }

    data_fa = pd.DataFrame(df)

elif (number_artists > 50):
    n = int(number_artists/50)
    rest = number_artists - n*50
    artists_names_fa = []
    artists_genres_fa = []
    artists_ids_fa = []
    artists_followers_fa = []
    following = (wide.user_following(50))
    following = following['artists']['items']
    index=0
    for i in range(1, len(following)+1):
        artists_names_fa.append(following[index]['name'])
        artists_genres_fa.append(following[index]['genres'])
        artists_ids_fa.append(following[index]['id'])
        artists_followers_fa.append(following[index]['followers']['total'])
        index += 1
    time.sleep(2)
    number_artists -= 50
    x=1
    while number_artists > 49 :
        for i in range(2, n+1):
            following[x] = (wide.user_following(50, after=artists_ids_fa[-1]))
            following[x] = following[x]['artists']['items']
            index=0
            for i in range(1, len(following[x])+1):
                artists_names_fa.append(following[x][index]['name'])
                artists_genres_fa.append(following[x][index]['genres'])
                artists_ids_fa.append(following[x][index]['id'])
                artists_followers_fa.append(following[x][index]['followers']['total'])
                index += 1
            x += 1
            time.sleep(2)
            number_artists -= 50
    else:
        if rest > 0 :
            following_rest = wide.user_following((rest), after=artists_ids_fa[-1])
            following_rest = following_rest['artists']['items']
            index=0
            for i in range(1, len(following_rest)+1):
                artists_names_fa.append(following_rest[index]['name'])
                artists_genres_fa.append(following_rest[index]['genres'])
                artists_ids_fa.append(following_rest[index]['id'])
                artists_followers_fa.append(following_rest[index]['followers']['total'])
                index += 1

    df = {'Artist': [i for i in artists_names_fa],
        'Genre': [i for i in artists_genres_fa],
        'Followers': [i for i in artists_followers_fa]
        }
    data_fa = pd.DataFrame(df)

fig_fa = px.scatter(x=data_fa["Followers"], size=data_fa["Followers"], color=data_fa["Artist"], hover_name=data_fa["Artist"],
                    labels={'x': 'Followers', 'y': 'Position', 'color':'Artist', 'size':'Followers'})
fig_fa.update_layout(height=1000)
fig_fa.update_traces(textfont_size=10, cliponaxis=False)

#Recently Played
if number_songs < 51:
    recent = (wide.recently_played(number_songs))
    recent = recent['items']
    artists_names = []
    songs_titles = []
    songs_albums = []
    albums_release = []
    last_played = []
    song_ids=[]
    timestamp = []
    index=0
    for i in range(1, len(recent)+1):
        artists_names.append(recent[index]['track']['artists'][0]['name'])
        song_ids.append(recent[index]['track']['id'])
        songs_titles.append(recent[index]['track']['name'])
        songs_albums.append(recent[index]['track']['album']['name'])
        albums_release.append(recent[index]['track']['album']['release_date'][0:4])
        last_played.append(recent[index]['played_at'][0:10] + ' - ' + recent[index]['played_at'][11:19])
        timestamp.append(recent[index]['played_at'])

        index += 1

    df = {'Song Title': [i for i in songs_titles],
          'Artist': [i for i in artists_names],
          'Album': [i for i in songs_albums],
          'Release date': [i for i in albums_release],
          'Last Played': [i for i in last_played]
        }
    data_rp = pd.DataFrame(df)
    df = data_rp
    position = [i for i in range(1,len(df)+1)]
    df['Position'] = position
    fig_rp = px.bar(df, x='Position', y='Artist', color="Album", text='Song Title', title=('Last plays'))
    fig_rp.update_layout(height=1000)
    fig_rp.update_traces(textfont_size=10, cliponaxis=False)

time.sleep(3)

number_artists_2 = 50

#Top Artists
if number_artists_2 < 51:
    following = (wide.top_artists(number_artists_2, time_range=time_range))
    following = following['items']
    #st.write(following)
    artists_names_top = []
    artists_genres_top = []
    artists_ids_top = []
    artists_url_top = []
    artists_pic_top = []
    index=0
    for i in range(1, len(following)+1):
        artists_names_top.append(following[index]['name'])
        artists_genres_top.append(following[index]['genres'])
        artists_ids_top.append(following[index]['id'])
        artists_url_top.append(following[index]['external_urls']['spotify'])
        artists_pic_top.append(following[index]['images'][1]['url'])
        index += 1

    df = {'Artist': [i for i in artists_names_top],
        'Genre': [i for i in artists_genres_top],
        'URL': [i for i in artists_url_top]
        }
    data_ta = pd.DataFrame(df)
    df = data_ta
    labels = [i for i in range(1,len(df)+1)]
    df['Position'] = labels
    fig_ta = px.bar(df, x='Position', y='Artist', color="Artist", text='Genre', title=(time_select+' favorite artists selection'))
    fig_ta.update_layout(height=1000)
    fig_ta.update_traces(textfont_size=10, cliponaxis=False)

time.sleep(3)

#Top Tracks
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
    data_tt = pd.DataFrame(df)
    df = data_tt
    position = [i for i in range(1,len(df)+1)]
    df['Position'] = position
    fig_tt = px.bar(df, x='Position', y='Artist', color="Album", text='Song Title', title=(time_select+' favorite songs selection'))
    fig_tt.update_layout(height=1000)
    fig_tt.update_traces(textfont_size=10, cliponaxis=False)

#Displays

#Full DF display
st.title(':violet[Here are your lists!]')
st.write('')
tab1, tab2, tab3, tab4 = st.tabs(["Followed Artists", "Recently Played", ("Top Artists - " +time_select), ("Top Tracks - " +time_select)])
with tab1:
    st.dataframe(data_fa, use_container_width=True)
    if fa_total > len(data_fa):
        st.write('Displaying the total number of your followed artists: '+str(len(data_fa)) + ' artist(s)')
    else:
        st.write('Displaying ' +str(len(data_fa)) + ' artist(s)')

with tab2:
    st.dataframe(data_rp, use_container_width=True)
    st.write('Displaying last ' +str(len(data_rp)) + ' played song(s).')

with tab3:
    st.dataframe(data_ta, use_container_width=True)
    st.write('Displaying ' +str(len(data_ta)) + ' artist(s)')

with tab4:
    st.dataframe(data_tt, use_container_width=True)
    st.write('Displaying ' +str(len(data_tt)) + ' song(s)')

st.divider()

#Top 5s display
st.title(':violet[Your Top 5 Artists and Tracks]')
st.write('')
tab1, tab2 = st.tabs([("Top 5 Artists - "+time_select), ("Top 5 Tracks - "+time_select)])

#Top 5 artists
with tab1:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.subheader(':violet[# 1]')
        button1 = st.button(artists_names_top[0], key=1)
        st.image(artists_pic_top[0])
        if button1:
            webbrowser.open(artists_url_top[0])
    with col2:
        st.subheader(':violet[# 2]')
        button2 = st.button(artists_names_top[1], key=2)
        st.image(artists_pic_top[1])
        if button2:
            webbrowser.open(artists_url_top[1])
    with col3:
        st.subheader(':violet[# 3]')
        button3 = st.button(artists_names_top[2], key=3)
        st.image(artists_pic_top[2])
        if button3:
            webbrowser.open(artists_url_top[2])
    with col4:
        st.subheader(':violet[# 4]')
        button1 = st.button(artists_names_top[3], key=4)
        st.image(artists_pic_top[3])
        if button1:
            webbrowser.open(artists_url_top[3])
    with col5:
        st.subheader(':violet[# 5]')
        button2 = st.button(artists_names_top[4], key=5)
        st.image(artists_pic_top[4])
        if button2:
            webbrowser.open(artists_url_top[4])
#Top 5 tracks
with tab2:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.subheader(':violet[# 1]')
        st.subheader(songs_titles[0])
        st.subheader('')
        st.write('by '+artists_names[0])
        button_a = st.button(songs_albums[0], key=6)
        st.subheader('')
        st.image(albums_pic[0])
        if button_a:
            webbrowser.open(albums_url[0])
    with col2:
        st.subheader(':violet[# 2]')
        st.subheader(songs_titles[1])
        st.subheader('')
        st.write('by '+artists_names[1])
        button_b = st.button(songs_albums[1], key=7)
        st.subheader('')
        st.image(albums_pic[1])
        if button_b:
            webbrowser.open(albums_url[1])
    with col3:
        st.subheader(':violet[# 3]')
        st.subheader(songs_titles[2])
        st.subheader('')
        st.write('by '+artists_names[2])
        button_c = st.button(songs_albums[2], key=8)
        st.subheader('')
        st.image(albums_pic[2])
        if button_c:
            webbrowser.open(albums_url[2])
    with col4:
        st.subheader(':violet[# 4]')
        st.subheader(songs_titles[3])
        st.subheader('')
        st.write('by '+artists_names[3])
        button_d = st.button(songs_albums[3], key=9)
        st.subheader('')
        st.image(albums_pic[3])
        if button_d:
            webbrowser.open(albums_url[3])
    with col5:
        st.subheader(':violet[# 5]')
        st.subheader(songs_titles[4])
        st.subheader('')
        st.write('by '+artists_names[4])
        button_e = st.button(songs_albums[4], key=10)
        st.subheader('')
        st.image(albums_pic[4])
        if button_e:
            webbrowser.open(albums_url[4])
st.divider()
#Graphs
st.title(':violet[Your Graphs]')
st.write('')
top5artists= "Top 5 Artists - " + time_select
top5songs= "Top 5 Tracks - " + time_select
tab1, tab2, tab3, tab4 = st.tabs(["Followed Artists", "Recently Played", top5artists, top5songs])

with tab1:
    st.plotly_chart(fig_fa, use_container_width=True, height=1000)
with tab2:
    st.plotly_chart(fig_rp, use_container_width=True, height=1000)
with tab3:
    st.plotly_chart(fig_ta, use_container_width=True, height=1000)
with tab4:
    st.plotly_chart(fig_tt, use_container_width=True, height=1000)
