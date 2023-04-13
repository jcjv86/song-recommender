'''
Program variables can be set on config.py file:
-client_id and client_secret.
-exported_files folder (default within script folder).
-log file name and location (default status.log, in script folder).
-source songs database for which we want to get IDs and features.

Other options that can be set on this script:
-Song ID and Song Features dfs names can be set on lines 72 and 97 respectively. They will be saved by default on the exported_files folder.
-Final concatenated df name can be set in line 110, default final_db.csv (within exported_files folder).

Access log last 2 lines (will display time left and number of songs remaining):
grep "INFO" status.log | tail -2

Run the script remotely in a Raspberry Pi (make sure to be in the same folder as the script and that the config file is there too).
ssh hostname "python3 spotify_raspberrypi_remote.py&"
'''

import numpy as np; import pandas as pd; import spotipy; import json; from spotipy.oauth2 import SpotifyClientCredentials; import time; import os; import logging; import sys
sys.path.append('./')
from config import client_id as client_id
from config import client_secret as client_secret
from config import exported_files as exported_files
from config import log_file as log_file
from config import timer as timer

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

try: os.rmdir(exported_files)
except: pass

try: os.mkdir(exported_files)
except: pass

logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.INFO)

def search_song(df, timer):
    df_id = df[(df['title']!= 'na')]
    df_id = df_id[(df_id['artist']!= 'na')]
    df_id['search'] = df_id['title'] + ', ' + df_id['artist']
    search = list(df_id['search'])
    original_n = len(search)
    df_id = df_id.drop(['search'], axis=1)

    los = []
    counter = len(search)+1
    logging.info('Getting song IDs\n')

    for i in search:
        counter -= 1
        seconds = (counter * timer)
        remaining = time.strftime("%H:%M:%S", time.gmtime(seconds))
        logging.info('Songs remaining: %s', counter)
        logging.info('Time left (approx): %s',remaining)
        time.sleep(timer)

        try:
            x= sp.search(q=i, limit=5)
            if x: los.append(x['tracks']['items'][1]['id'])

        except:
            los.append('na')

    df_id['id'] = los
    df_id = df_id[(df_id['id']!= 'na')]
    final_n = df_id.shape[0]
    not_found = original_n-final_n

    logging.info('\n\nSongs not found: %s', not_found)
    logging.info('\n\n\n\n')

    df_id.to_csv('/exported_files/db_id.csv', index = False)
    return df_id

def get_audio_features(df_id, timer):
    list_of_songs = list(df_id['id'])
    original_n = len(list_of_songs)
    los=[]
    counter = len(list_of_songs)+1
    logging.info('Getting song features\n')
    for i in list_of_songs:
        counter -= 1
        seconds = (counter * timer)
        remaining = time.strftime("%H:%M:%S", time.gmtime(seconds))
        logging.info('Songs remaining: %s', counter)
        logging.info('Time left (approx): %s',remaining)
        time.sleep(timer)
        try:
            x = sp.audio_features(i)[0]
            if x: los.append(x)
        except:
            pass
    df_feat = pd.DataFrame(los)
    final_n = df_feat.shape[0]
    not_found = original_n-final_n
    logging.info('\n\nSongs not found: %s', not_found)
    df_feat.to_csv('/exported_files/db_feat.csv', index = False)
    return df_feat

def concat_id_feat(df_id, df_feat):
    original_n = df_id.shape[0]
    df_id['check'] = df_id.id.isin(df_feat.id)
    df_id = df_id[(df_id['check'] == True)]
    df_id.reset_index(drop=True, inplace=True)
    df_id = df_id.drop(['check'], axis=1)
    final_n = df_id.shape[0]
    not_found = original_n-final_n
    logging.info('\n\nSongs not found: %s', not_found)
    extended_df = pd.concat([df_id, df_feat], axis=1)
    extended_df.to_csv('/exported_files/final_db.csv', index=False)
    logging.info('\n\nFinal dataframe created successfully. Program will now terminate.')

def spotifier(df, timer):
    df_id = search_song(df, timer)
    df_feat = get_audio_features(df_id, timer)
    concat_id_feat(df_id, df_feat)

df = pd.read_csv(source)
spotifier(df, timer)
