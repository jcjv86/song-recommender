import streamlit as st
st.set_page_config(page_title='WIDE - Home', page_icon=':headphones:', layout="wide", initial_sidebar_state="auto", menu_items=None)

st.image('../src/img/logo.png', width=650)
st.title('Opening your ears to a wide world of music :headphones:')
st.divider()
st.subheader('*Tired of always listening to the same music?*')
st.subheader(':red[**TRY WIDE!**]')
st.write('You can now find your new favorite songs according to the features or to the related artists!!!')
st.divider()

st.write('*What makes us different?*')

st.write('''
1. :violet[Precision:] \n\nWith a vast library of songs across all genres, our app offers a personalized music experience that tailors recommendations to your unique preferences.

2. :violet[Spotify link of your recommendation:] \n\nWe provide a direct link of the recommendation so you can listen right away to your future favorite songs

3. :violet[Choose the number of recommendations:] \n\nWith WIDE you can choose the number of recommendations you want. You can have one track or an entire list.

4. :violet[Features layout:] :red[**(UNDER DEVELOPMENT)**] \n\nWe know that is important to understand what features you love of your music. That's why we integrate a plot to show you what are the things you love.

5. :violet[Save your songs into a new or already existing Spotify playlist:] :red[**(UNDER DEVELOPMENT)**] \n\nDon't lose any second and listen to your songs straight away!

''')
