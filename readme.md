![Alt text](src/img/logo_back.png?raw=true "Title")

 #### The song recommender

## Opening your ears to a wide world of music

*Tired of listening always to the same music?*

**TRY Wide!**

## *What makes us different?*

1. **Precision**<br>
With a vast library of songs across all genres, our app offers a personalized music experience that tailors recommendations to your unique preferences.

2. **Spotify link of your recommendation**<br>
We provide a direct link of the recommendation so you can listen  right away your future favorite songs

3. **Choose the number of recommendations**<br>
With Wide you can choose the amount of recommendations you want. You can have one track or an entire list.

4. **Features layout**<br>
We know that is important to understand what features you love of your music. Thats why we integrate a plot to show you what are the things  you love.

#

### Updates

- Added extra databases with bigger number of songs and more diverse styles (original had 5k, newest has 37k)
- Included script to fetch song ID and features that runs remotely in a Raspberry Pi via SSH (src/lib/spotify_raspberrypi_remote.py).
- Spotify API credentials can be provided on config script (src/lib/config.py).
- Clustering now considers tempo as a weight so recommendations have a similar tempo.
- Work in progress - multipage streamlit app.

## Installation guide:

Open a terminal and:

1- Clone repository into desired folder: <br> git clone https://github.com/jcjv86/song-recommender.git<br><br>
2- Move into repository folder: <br> cd song-recommender<br><br>
3- Create virtual environment: <br> python3 -m venv ./venv<br><br>
4- Acivate virtual environment: <br> source ./venv/bin/activate<br><br>
5- Install requirements: <br> pip install -r requirements.txt<br><br>
6- Move into app folder: <br> cd app<br><br>
7- Run app: <br> streamlit Home.py
