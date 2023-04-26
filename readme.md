![Alt text](src/img/logo_back.png?raw=true "Title")

 #### The song recommender

## Opening your ears to a wide world of music

*Tired of listening always to the same music?*

**Take a walk on the WIDE side!**

## *What makes us different?*

1. **Precision**<br>
With a vast library of songs across all genres, our app offers a personalized music experience that tailors recommendations to your unique preferences.

2. **Spotify link of your recommendations**<br>
We provide a direct link of the recommendations so you can listen right away to your future favorite songs

3. **Choose the number of recommendations**<br>
With WIDE you can choose the number of recommendations you want. You can have one track or an entire list (up to 20 songs).

4. **Features layout**<br>
We know that is important to understand what features you love from your music. That's why we integrate a plot to show you what are the things you love.

5. **Save your songs into an existing Spotify playlist**<br>
Don't lose any second and listen to your songs straight away!

### WIDE can run on the song recommender jupyter notebook or on the multipage streamlit app (this last one includes new features like recommendations based on related artists and export the recommendations into a playlist).
### You can check the app demo and instructions on the app folder readme file.

## Installation guide:

Open a terminal and:

1. Clone repository into desired folder (move to the folder and write): <br><br> git clone https://github.com/jcjv86/song-recommender.git<br><br>
2. Move into newly created repository folder inside the previous one: <br><br> cd song-recommender<br><br>
3. Create virtual environment: <br><br> python3 -m venv ./venv<br><br>
4. Acivate virtual environment: <br><br> source ./venv/bin/activate<br><br>
5. Install requirements: <br> pip install -r requirements.txt<br><br>
6. If you want to run the original program from the jupyer notebook, you can find both the original and the extended (which uses the song tempo as a weight to recommend songs with similar tempo) into the /notebooks folder.<br><br>
7. If you want to use the app, move into app folder: <br><br> cd app<br><br>
8. Configure program settings on app/config/config.py file.<br><br>
9. Run app: <br><br> streamlit Home.py

<br><br>
#### Updates

- New search option: Related artists! You can click on the names and you will be redirected to the artist profile page in Spotify.
- Added extra databases with bigger number of songs and more diverse styles (original had 5k, newest has 37k)
- Included script to fetch song ID and features that runs remotely in a Raspberry Pi via SSH (src/lib/spotify_raspberrypi_remote.py).
- Program settings on config script in src/lib/config.py file. Needed to use the app!
- Clustering now considers tempo as a weight so recommendations in the search by features page have a similar tempo.


