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
import webbrowser
import random
st.set_page_config(page_title='WIDE - Related Artist Search', page_icon=':singer:', layout="wide", initial_sidebar_state="auto", menu_items=None)

from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private"))


st.image('../src/img/logo.png', width=650)

def make_clickable(link):
    return '<a href="{0}">{0}</a>'.format(link)

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

    user_selection = st.radio('Please select one from the below options (song - album - artist)', (selection_lst[0], selection_lst[1], selection_lst[2], selection_lst[3], selection_lst[4]))
    if user_selection == selection_lst[0]:
        st.image(pics_lst[0], width=300)
        return artists_id[0]
    elif user_selection == selection_lst[1]:
        st.image(pics_lst[1], width=300)
        return artists_id[1]
    elif user_selection == selection_lst[2]:
        st.image(pics_lst[2], width=300)
        return artists_id[2]
    elif user_selection == selection_lst[3]:
        st.image(pics_lst[3], width=300)
        return artists_id[3]
    elif user_selection == selection_lst[4]:
        st.image(pics_lst[4], width=300)
        return artists_id[4]
    else:
        st.write('Please select one song')

st.divider()

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
    st.write(':violet[Your search:]', title, ':violet[by]', artist)
    st.divider()
    st.title(':violet[Search results:]')
    title = title.lower()
    artist = artist.lower()
    results = search_song(title, artist)
    artist_id = user_select(results)
    st.divider()

    #Related artists search
    related_artists_id = []
    related_artists_name = []
    related_artists_pic = []
    related_artists_url = []
    songs_search = []
    index = 0
    related = sp.artist_related_artists(artist_id)
    for i in range(1, len(related['artists'])+1):
                       related_artists_id.append(related['artists'][index]['id'])
                       related_artists_url.append(related['artists'][index]['external_urls']['spotify'])
                       related_artists_name.append(related['artists'][index]['name'])
                       related_artists_pic.append(related['artists'][index]['images'][2]['url'])
                       index += 1

    #Related artists songs search
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

    #Related artists Song URI search (pure track URI needed, previous search only provides artists track URI)
    ra_song_uri = []
    index=0
    for i in range(1, len(ra_song_id)+1):
        ra_tracks = sp.track(track_id = ra_song_id[index])
        ra_song_uri.append(ra_tracks['uri'])
        index += 1

    st.title(':violet[**Related artists**]')
    st.caption('Click on their name to be redirected to their Spotify profile.')
    st.title('')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        button1 = st.button(related_artists_name[0])
        st.image(related_artists_pic[0])
        if button1:
            webbrowser.open(related_artists_url[0])

    with col2:
        button2 = st.button(related_artists_name[1])
        st.image(related_artists_pic[1])
        if button2:
            webbrowser.open(related_artists_url[1])

    with col3:
        button3 = st.button(related_artists_name[2])
        st.image(related_artists_pic[2])
        if button3:
            webbrowser.open(related_artists_url[2])

    with col4:
        button4 = st.button(related_artists_name[3])
        st.image(related_artists_pic[3])
        if button4:
            webbrowser.open(related_artists_url[3])

    with col5:
        button5 = st.button(related_artists_name[4])
        st.image(related_artists_pic[4])
        if button5:
            webbrowser.open(related_artists_url[4])

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        button6 = st.button(related_artists_name[5])
        st.image(related_artists_pic[5])
        if button6:
            webbrowser.open(related_artists_url[5])

    with col2:
        button7 = st.button(related_artists_name[6])
        st.image(related_artists_pic[6])
        if button7:
            webbrowser.open(related_artists_url[6])

    with col3:
        button8 = st.button(related_artists_name[7])
        st.image(related_artists_pic[7])
        if button8:
            webbrowser.open(related_artists_url[7])

    with col4:
        button9 = st.button(related_artists_name[8])
        st.image(related_artists_pic[8])
        if button9:
            webbrowser.open(related_artists_url[8])

    with col5:
        button10 = st.button(related_artists_name[9])
        st.image(related_artists_pic[9])
        if button10:
            webbrowser.open(related_artists_url[9])

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        button11 = st.button(related_artists_name[10])
        st.image(related_artists_pic[10])
        if button11:
            webbrowser.open(related_artists_url[10])

    with col2:
        button12 = st.button(related_artists_name[11])
        st.image(related_artists_pic[11])
        if button12:
            webbrowser.open(related_artists_url[11])

    with col3:
        button13 = st.button(related_artists_name[12])
        st.image(related_artists_pic[12])
        if button13:
            webbrowser.open(related_artists_url[12])

    with col4:
        button14 = st.button(related_artists_name[13])
        st.image(related_artists_pic[13])
        if button14:
            webbrowser.open(related_artists_url[13])

    with col5:
        button15 = st.button(related_artists_name[14])
        st.image(related_artists_pic[14])
        if button15:
            webbrowser.open(related_artists_url[14])

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        button16 = st.button(related_artists_name[15])
        st.image(related_artists_pic[15])
        if button16:
            webbrowser.open(related_artists_url[15])

    with col2:
        button17 = st.button(related_artists_name[16])
        st.image(related_artists_pic[16])
        if button17:
            webbrowser.open(related_artists_url[16])

    with col3:
        button18 = st.button(related_artists_name[17])
        st.image(related_artists_pic[17])
        if button18:
            webbrowser.open(related_artists_url[17])

    with col4:
        button19 = st.button(related_artists_name[18])
        st.image(related_artists_pic[18])
        if button19:
            webbrowser.open(related_artists_url[18])

    with col5:
        button20 = st.button(related_artists_name[19])
        st.image(related_artists_pic[19])
        if button20:
            webbrowser.open(related_artists_url[19])

    st.divider()

    st.title(":violet[Here's your playlist!]")
    st.caption('One random song picked from each one of the related artists - 20 songs in total')
    st.title('')
    button_playlist = st.button('Click to add tracks to playlist and open in browser - see selected songs below :headphones:')
    if button_playlist:
        playlist_items_search = sp.playlist_items(playlist_id)
        playlist_items = []
        index=0
        for i in range(1, len(playlist_items_search['items'])+1):
            playlist_items.append(playlist_items_search['items'][index]['track']['id'])
            index += 1
        sp.playlist_remove_all_occurrences_of_items(playlist_id, playlist_items)
        sp.playlist_add_items(playlist_id, items=ra_song_url)
        webbrowser.open(playlist_url)

    st.title('')

    song_number = [i for i in range(1,21)]
    recommended_songs_df = pd.DataFrame(song_number)
    recommended_songs_df.rename(columns={0:'No.'}, inplace=True)
    recommended_songs_df['Song Title'] = ra_song_name
    recommended_songs_df['Album'] = ra_album_name
    recommended_songs_df['Artist'] = ra_artist_name
    recommended_songs_df['URL'] = ra_song_url
    recommended_songs_df['URL'] = recommended_songs_df['URL'].apply(make_clickable)
    st.write(HTML(recommended_songs_df.to_html(index=False,escape=False)))


    #Add to queue button - needs further work

    #button_queue = st.button('Click to add tracks to queue and play')
    #if button_queue:
        #webbrowser.open('https://open.spotify.com/')
        #time.sleep(2)
        #device_search = sp.devices()
        #st.write(device_search)
        #device = device_search['devices'][0]['id']
        #time.sleep(2)
        #sp.start_playback(device, context_uri='playlist', offset={'uri':ra_song_uri[0]}, uris=ra_song_uri)

st.title('')
st.title('')
st.title('')
with st.expander('Our inspiration - searched this song in all the numerous tests. Thanks Iggy! \n\n:crocodile:'):
    st.video('https://www.youtube.com/watch?v=jQvUBf5l7Vw')
