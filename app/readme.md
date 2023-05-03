 ![Alt text](../src/img/logo_back.png?raw=true "Title")

 #### The song recommender

## Opening your ears to a wide world of music

*Tired of listening always to the same music?*

**Take a walk on the WIDE side!**

# Streamlit app configuration

This app uses Python's Spotipy library. First of all, you will have to create a new app for it on the [Spotify for Developers website](https://developer.spotify.com/)<br>

You can set the program variables in the configuration file (on the app/config/config.py file):<br>

- User ID: Your Spotify User ID. On Spotify Web, click on your name, then profile. The user ID is on the URL:<br> (open.spotify.com/user/USER_ID)
- Client ID: Client ID, found on Spotify for Developers Dashboard, on the app Settings.
- Client Secret: Client Secret, found on Spotify for Developers Dashboard, on the app Settings.
- Playlist id: The playlist ID where you want to save your searches. Found in the URL:<br> (open.spotify.com/playlist/PLAYLIST_ID)
- Timer: In order to avoid temporary bannign from Spotify, you should not make more than 10 calls in a 30 sec window. Timer is set by default to 3 seconds to ensure this (timers are set on the playlist generation features that are activated via click). <br>Modify at your own risk!

In order for the app to access some of the functions, user has to authorize some scopes (or permissions) for the app.<br>

The first time you run the app it will ask your permission for these app scopes, which are essential for example to check the playlist you use to save the songs of the searches, and to delete the contents of it after you make another search and add new tracks to it.<br>

After you accept, the app will automatically open a new tab in your browser. It will show as connection failed, but this is not important. You need to copy the full URL of that tab and paste it into the terminal that is running the streamlit app. It will be displayed as shown in the below pictures:<br>

#### New tab:
![Alt text](../src/img/authentication1.png?raw=true "Title")
#### Console:
![Alt text](../src/img/authentication2.png?raw=true "Title")

<br>

After you copied and pasted this URL the app should work (if there is an error message and the terminal keeps asking for the URL keep pasting it until it picks it up, can take a few tries, eventually stop the app and run it again to start again).<br>

### Congrats! You should be able to use the app now.

# App demo

### Home page:
![Alt text](./pics/wide_home.png?raw=true "Title")
### WIDE - Search by Song Features
![Alt text](./pics/wide_feat_01.png?raw=true "Title")
![Alt text](./pics/wide_feat_02.png?raw=true "Title")
![Alt text](./pics/wide_feat_03.png?raw=true "Title")
![Alt text](./pics/wide_feat_04.png?raw=true "Title")
![Alt text](./pics/wide_feat_05.png?raw=true "Title")
### Song features playlist
![Alt text](./pics/wide_feat_playlist.png?raw=true "Title")
### WIDE - Search by Related Artists
![Alt text](./pics/wide_rltd_01.png?raw=true "Title")
![Alt text](./pics/wide_rltd_02.png?raw=true "Title")
![Alt text](./pics/wide_rltd_03.png?raw=true "Title")
### Related artists playlist
![Alt text](./pics/wide_rltd_playlist.png?raw=true "Title")
### WIDE - User Info
![Alt text](./pics/wide_user_info.png?raw=true "Title")
### WIDE - Followed Artists
![Alt text](./pics/wide_followed_artists_01.png?raw=true "Title")
![Alt text](./pics/wide_followed_artists_02.png?raw=true "Title")
