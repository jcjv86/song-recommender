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
