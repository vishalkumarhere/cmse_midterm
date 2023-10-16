import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV files
spotify_data = pd.read_csv('spotify_top_songs.csv')
kworb_data = pd.read_excel('kworb_global.xlsx')

# Create a Streamlit app
st.title("Data Visualization App")

# Filters with default "Select All" option
selected_rows = st.multiselect("Select Rows", spotify_data['Title'].unique())
selected_country = st.multiselect("Select Country", kworb_data.columns[3:], key='country_filter')
selected_song = st.multiselect("Select Song", kworb_data['Title'].unique(), key='song_filter')

# Create a filter dynamically based on selected countries
country_filter = ['US']
# country_filters = [kworb_data[country].isin(selected_country) for country in selected_country]
# country_filter = pd.concat(country_filters, axis=1).any(axis=1)

# Apply filters to the data
filtered_spotify_data = spotify_data[spotify_data['Title'].isin(selected_rows)]
filtered_kworb_data = kworb_data[country_filter & kworb_data['Title'].isin(selected_rows)]

# Plot charts
st.header("Charts")
st.subheader("Spotify Top Songs")
st.write(filtered_spotify_data)

# Plot charts for Spotify data (example)
fig = px.bar(filtered_spotify_data, x='Title', y='Streams', title="Spotify Top Songs")
st.plotly_chart(fig)

st.subheader("KWORB Global Data")
st.write(filtered_kworb_data)

# Plot charts for KWORB data (example)
fig = px.bar(filtered_kworb_data, x='Title', y='Streams', title="KWORB Global Data")
st.plotly_chart(fig)
