import pandas as pd
import sys
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
from Recommender import *
import webbrowser
import random
from spotipy.oauth2 import SpotifyOAuth


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id,
                                               client_secret,
                                               redirect_uri='https://localhost:8080',
                                               scope="user-modify-playback-state user-read-playback-state playlist-modify-public playlist-modify-private user-top-read user-follow-read user-read-recently-played"))

class Stats():
    #def __init__(self):
        #self.client_id = client_id

    def user_info(self):
        user_info = sp.current_user()
        return user_info

    def user_following(self, limit, after=None):
       followed_artists = sp.current_user_followed_artists(limit, after)
       return followed_artists

    def recently_played(self, limit, after=None, before=None):
        recently_played = sp.current_user_recently_played(limit, after, before)
        return recently_played

    def top_artists(self, limit, offset=0, time_range='medium_term'):
        top_artists = sp.current_user_top_artists(limit, offset, time_range)
        return top_artists

    def top_tracks(self,limit, offset=0, time_range='medium_term'):
        top_tracks = sp.current_user_top_tracks(limit, offset, time_range)
        return top_tracks
