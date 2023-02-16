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
from IPython.display import HTML

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                           client_secret= client_secret))

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
    counter = 1
    index = 0
    songs = []
    for i in range(1, len(results['tracks']['items'])+1):
        print(counter,'.\n')
        print('song name: ',results['tracks']['items'][index]['name'])
        print('artist name: ',results['tracks']['items'][index]['artists'][0]['name'])
        print('url: ',base_url+results['tracks']['items'][index]['id'])
        print()
        songs.append(results['tracks']['items'][index]['id'])
        counter += 1
        index += 1
        
    user_selection = str(input('\n\nWhich song would you prefer? Please enter a number from the list above: \n'))
    valid_values = [str(i) for i in range (1, len(results['tracks']['items'])+1)]
    while user_selection not in valid_values:
        user_selection = str(input('Invalid value. Please enter Please enter a number in the list!: \n'))
    print()
    if user_selection == '1':
        return songs[0]
    elif user_selection == '2':
        return songs[1]
    elif user_selection == '3':
        return songs[2]
    elif user_selection == '4':
        return songs[3]
    elif user_selection == '5':
        return songs[4]


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

def make_clickable(link):
    return '<a href="{0}">{0}</a>'.format(link)

def selector(final_scaled, database, song_id, final):
    
    song_recomender_df = pd.concat([database[['title','artist','id','source']],final_scaled],axis=1)
    song_recomender_df_hot = song_recomender_df[(song_recomender_df['source'] == 'H')]
    song_recomender_df_nonhot = song_recomender_df[(song_recomender_df['source'] == 'N')]
    
    if song_id in song_recomender_df_hot:
        song_recomender_test = song_recomender_df_hot[(song_recomender_df_hot['cluster'] == final)].sample(5)
    else:
        song_recomender_test = song_recomender_df_nonhot[(song_recomender_df_nonhot['cluster'] == final)].sample(5)
    
    song_recomender_test = song_recomender_test[['title','artist', 'id']]
    base_url = 'https://open.spotify.com/track/'
    id_list = list(song_recomender_test['id'])
    url_list = [base_url + i for i in id_list]    
    song_recomender_test['url'] = url_list
    song_recomender_test['url'] = song_recomender_test['url'].apply(make_clickable)
    
    
    song_recomender_test = song_recomender_test.drop(['id'], axis=1)
    print()
    print('Here are 5 similar songs to your selection: \n')
    display(HTML(song_recomender_test.to_html(escape=False)))


def song_recommender(df):
    #Get song id
    database = df
    results = search_song()
    
    #Make user select
    song_id = user_select(results)
    
    #Get audio features of the song and display them
    df = get_audio_features(song_id)
    
    #Scale song feat by adding it to our database and then returning it scaled.
    df2 = database[['danceability','energy', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
       'valence', 'tempo']]
    df3 = pd.concat([df2,df],axis=0)
    df_scaled = scaler(df3)
    final = clustering(df_scaled)

    final_scaled = df_scaled.iloc[0:-1]
    selector(final_scaled, database, song_id, final)