import pandas as pd
import sys
sys.path.insert(1, '/home/juan/Documents/')
import time
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from credentials import *
import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                           client_secret= client_secret))

database = pd.read_csv('database.csv')

def search_song():
    title = str(input('Please enter song title: ')).lower()
    artist = str(input('Please enter artist name: ')).lower()
    print()
    try:
        results = sp.search(q=title+','+artist, limit=5)
        #song_id = results['tracks']['items'][-1]['id']
        return results
    except: 
        return 'na'

def user_select(results):

    base_url = 'https://open.spotify.com/track/'
    
    print('1.')
    print('song name: ',results['tracks']['items'][0]['name'])
    print('artist name: ',results['tracks']['items'][0]['artists'][0]['name'])
    song_1 = results['tracks']['items'][0]['id']
    print('url: ',base_url+results['tracks']['items'][0]['id'])
    print()
    print('2.')
    print('song name: ',results['tracks']['items'][1]['name'])
    print('artist name: ',results['tracks']['items'][1]['artists'][0]['name'])
    song_2 = results['tracks']['items'][1]['id']
    print(base_url+results['tracks']['items'][1]['id'])
    print()
    print('3.')
    print('song name: ',results['tracks']['items'][2]['name'])
    print('artist name: ',results['tracks']['items'][2]['artists'][0]['name'])
    song_3 = results['tracks']['items'][2]['id']
    print('url: ',base_url+results['tracks']['items'][2]['id'])
    print()
    print('4.')
    print('song name: ',results['tracks']['items'][3]['name'])
    print('artist name: ',results['tracks']['items'][3]['artists'][0]['name'])
    song_4 = results['tracks']['items'][3]['id']
    print('url: ',base_url+results['tracks']['items'][3]['id'])
    print()
    print('5.')
    print('song name: ',results['tracks']['items'][4]['name'])
    print('artist name: ',results['tracks']['items'][4]['artists'][0]['name'])
    song_5 = results['tracks']['items'][4]['id']
    print('url: ',base_url+results['tracks']['items'][4]['id'])


    user_selection = str(input('\n\nWhich song would you prefer? Please enter number 1-5: \n'))
    valid_values = ['1', '2', '3', '4', '5']
    while user_selection not in valid_values:
        user_selection = str(input('Invalid value. Please enter Please enter a number 1-5: \n'))

    print()
    if user_selection == '1':
        return song_1
    elif user_selection == '2':
        return song_2
    elif user_selection == '3':
        return song_3
    elif user_selection == '4':
        return song_4
    elif user_selection == '5':
        return song_5
    
def get_audio_features(song_id):
    my_dict = {}
    los=[]
    try:
        x = sp.audio_features(song_id)[0]
        if x: los.append(x)
    except:
        pass
    df = pd.DataFrame(los)
    df = df[['danceability','energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo']]
    return df

def scaler(df):
    X = df.copy()
    scaler = StandardScaler()
    scaler.fit(X)
    X_scaled = scaler.transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns = X.columns)
    return X_scaled_df

def clustering(X_scaled_df):
    kmeans = KMeans(n_clusters=7, random_state=1234)
    kmeans.fit(X_scaled_df)
    clusters = kmeans.predict(X_scaled_df)
    pd.Series(clusters).value_counts().sort_index()
    X_scaled_df["cluster"] = clusters
    track_cluster = X_scaled_df.iloc[-1]
    final = track_cluster['cluster']
    return final

def song_reccomender():
    #Get song id
    results = search_song()
    
    #Make user select
    song_id = user_select(results)
    
    #Get audio features of the song and display them
    df = get_audio_features(song_id)
    
    #Scale song feat by adding it to our database and then returning it scaled.
    database = pd.read_csv('database.csv')
    df2 = database[['danceability','energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo']]
    df3 = pd.concat([df2,df],axis=0)
    df_scaled = scaler(df3)
        
    cluster = int(clustering(df_scaled))
    
    print('Song belongs to cluster', cluster)
    
