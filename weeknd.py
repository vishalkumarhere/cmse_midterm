import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV files
spotify_data = pd.read_csv('spotify_top_songs.csv')
kworb_data = pd.read_excel('kworb_global.xlsx')

# Create a Streamlit app
st.title("Data Visualization App")

# Filters with default "Select All" option
selected_rows = st.multiselect("Select Rows", spotify_data['Title'].unique(), default=spotify_data['Title'].unique())
selected_country = st.multiselect("Select Country", kworb_data.columns[5:], default=kworb_data.columns[5:])
selected_song = st.multiselect("Select Song", kworb_data['Title'].unique(), default=kworb_data['Title'].unique())

# Apply filters to the data
filtered_spotify_data = spotify_data[spotify_data['Title'].isin(selected_rows)]
filtered_kworb_data = kworb_data[kworb_data['Global'].isin(selected_country) & kworb_data['Title'].isin(selected_song)]

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
