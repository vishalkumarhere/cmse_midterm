import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px

# Load the CSV files
spotify_data = pd.read_csv("spotify_top_songs.csv")
weekend_data = pd.read_csv("theWeekndAf_final.csv")
kworb_data = pd.read_csv("kworb_global.csv")

# Title and Artist Introduction
st.title("The Weeknd Discography")
st.image("https://s3.amazonaws.com/media.thecrimson.com/photos/2020/04/02/211518_1343746.jpg", use_column_width=True)
st.write("The Weeknd, whose real name is Abel Tesfaye, is a Canadian singer, songwriter, and record producer. He is known for his distinctive voice and has released numerous hit songs and albums over the years.")

st.markdown("---")

# Create a Plotly Express bar chart to display the top 10 songs
st.subheader("Top 10 Most Streamed Songs by The Weeknd")
top_10_songs_chart = px.bar(
    spotify_data.head(10),
    x="Title",
    y="Streams",
    width=900,
    height=700,
    labels={"Title": "Song Title", "Streams": "Total Streams"}
)
st.plotly_chart(top_10_songs_chart)

st.markdown("---")

# Extract the year from the "Date" column and create a new column "Year"
kworb_data['Year'] = pd.to_datetime(kworb_data['Peak Date'], format='%d-%m-%y').dt.year

# Group the data by year and sum the streams for each year
yearly_streams = kworb_data.groupby('Year')['Streams'].sum().reset_index()

# Create a time series line plot using Plotly Express
st.header("Global Streams Over Time (Grouped by Year)")
global_streams_chart = px.line(
    yearly_streams,
    x="Year",
    y="Streams",
    labels={"Year": "Year", "Streams": "Global Streams"},
    # title="Global Streams Over Time (Grouped by Year)",
    width=900,  # Adjust the width as a percentage of the available space
    height=400,  # You can adjust the height as a fixed value or a percentage
)

st.plotly_chart(global_streams_chart)

st.markdown("---")

# Section: Audio Features Analysis
st.header("Audio Features Analysis")
st.write("To evaluate the different characteristics of each album, we will chose 5 audio features that are provided by Spotify's own algorithm")

# Subsection 1: Popularity
st.subheader("1. Popularity")
st.write("Popularity is a measure of how popular a song is, calculated by the total number of plays the track has had and how recent those plays are.")
st.write("A score of 1 indicates low popularity 👎, and a score of 100 means the song is trending 🔥.")

# Subsection 2: Danceability
st.subheader("2. Danceability")
st.write("Danceability is a measure of how danceable a track is, based on an algorithm in Spotify.")
st.write("A score of 0 means the song is not danceable 🥱, and a score of 1 means it's very danceable 🕺💃.")

# Subsection 3: Energy
st.subheader("3. Energy")
st.write("Energy is a measure of intensity, representing how energetic the track is.")
st.write("A score of 0 indicates low energy 💤, and a score of 1 means the song is full of energy 🔋.")

# Subsection 4: Tempo
st.subheader("4. Tempo")
st.write("Tempo refers to the speed of the beat in beats per minute (BPM).")
st.write("Typical BPM ranges for different music genres:")
st.write("- R&B: 60-80 BPM")
st.write("- Hip-hop: 85-115 BPM")
st.write("- Pop: 100-130 BPM")
st.write("- Rock: 110-140 BPM")

# Subsection 5: Valence
st.subheader("5. Valence")
st.write("Valence is a measure of the overall mood of a track.")
st.write("A score of 0 means the song has a sad mood 😢, and a score of 1 indicates a happy mood 😊.")

st.markdown("---")

# st.header('Distribution of Each Audio Feature')

# Extract the relevant columns from weekend_data
audio_features = weekend_data[["popularity", "danceability", "energy", "tempo", "valence"]]

# Create a for loop to plot the distributions of audio features
num_features = len(audio_features.columns)

# Define the number of columns and rows for the subplots
num_cols = 2
num_rows = (num_features + num_cols - 1) // num_cols

for i, feature in enumerate(audio_features.columns):
    if i % num_cols == 0:
        fig, axes = plt.subplots(1, num_cols, figsize=(12, 4))
    sns.histplot(audio_features[feature], kde=True, ax=axes[i % num_cols])
    axes[i % num_cols].set_title(feature.capitalize())
    if (i + 1) % num_cols == 0 or (i + 1) == num_features:
        st.pyplot(fig)

st.markdown("---")

# Create a heatmap of audio features
st.header("Audio Features Heatmap")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(audio_features.corr(), annot=True, vmin=-1, vmax=+1, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.markdown("---")

# Create a scatterplot of audio features
st.header("Scatterplot of Audio Features")
scatterplot = px.scatter_matrix(
    audio_features,
    dimensions=["popularity", "danceability", "energy", "tempo", "valence"]
)

scatterplot.update_layout(
    width=900,  # Adjust the width as needed
    height=900,  # Adjust the height as needed
)
st.plotly_chart(scatterplot)

st.markdown("---")

# Group the data by album name and calculate the mean of audio features within each group
grouped_data = weekend_data.groupby(['album_name'])[
    'popularity', 'danceability', 'energy', 'tempo', 'valence'].mean().reset_index()

# Create a graph with audio features by album name
st.header("Audio Features by Album Name")

# Define the audio features to plot
audio_features = ['popularity', 'danceability', 'energy', 'tempo', 'valence']

# Create a bar chart for each audio feature
for feature in audio_features:
    fig = px.bar(
        grouped_data,
        x='album_name',
        y=feature,
        title=f"{feature.capitalize()} by Album Name",
    )
    st.plotly_chart(fig)

st.markdown("---")

# Create a scatterplot between "popularity" and remaining audio features
st.header("Scatterplots: Popularity vs. Audio Features")

# Define the audio features to plot against popularity
audio_features = ["danceability", "energy", "tempo", "valence"]

# Create scatterplots for each audio feature
for feature in audio_features:
    fig = px.scatter(
        weekend_data,
        x="popularity",
        y=feature,
        title=f"Popularity vs. {feature.capitalize()}",
        labels={"popularity": "Popularity", feature: feature.capitalize()},
    )
    st.plotly_chart(fig)

st.markdown("---")

# Calculate the average of all audio features individually
average_features = weekend_data[["popularity", "danceability", "energy", "tempo", "valence"]].mean()

# Print out the average values
st.header("Average Audio Features")
st.write(average_features)

# Section: The Weeknd's Sound Evolution
st.header("The Weeknd's Sound Evolution")

st.markdown("Let's have a look at how The Weeknd's unique sounds evolve with each album. With every album, we can clearly see a progressive change in some of the audio features, while some are quite consistent throughout the albums.")

# Overall Tempo
st.subheader("Overall Tempo:")
st.markdown("🎵 (124 bpm)")
st.markdown("Looking at the average tempo of the albums, there is a consistency with the average being 124 bpm for all albums. This bpm typically falls in the Pop genre, although his music style is considered as alternative R&B, according to his Wikipedia page. (Reference: Figure titled 'The Evolution of The Weeknd's Sounds')")

# Overall Moods
st.subheader("Overall Moods:")
st.markdown("😢 (0.3/1)")
st.markdown("In terms of the overall mood of the albums, measured by the valence scores, his first debut album House of Balloons appears to be the most darkest, while Starboy is the most positive album. Nonetheless, the average valence score of 0.3 across all his albums indicates the reoccurring melancholy theme in every album that is consistent with the 'character' or the public image Abel creates for The Weeknd, along with the dark & sexual lyrics and his eccentric lifestyle. (References: Figure titled 'The Evolution of The Weeknd's Sounds', Table titled 'Summary of All Albums')")

# Overall Danceability and Energy
st.subheader("Overall Danceability and Energy:")
st.markdown("🧍 (0.6/1)")
st.markdown("The average danceability and energy score of 0.6 out of 1 across all albums also supports the perceived musical and character style of The Weeknd. Let's face it, they are not the go-to for dancing. His songs serve a completely different purpose 😈😉 (References: Figure titled 'The Evolution of The Weeknd's Sounds', Table titled 'Summary of All Albums')")

# Overall Popularity
st.subheader("Overall Popularity:")
st.markdown("🔥 (52/100)")
st.markdown("Lastly, there is a progressive growth in the average popularity of the tracks with every new album released. However, we see a big dip in popularity for Beauty Behind the Madness. Perhaps, the album did not get the right amount of exposure due to the mega success of the album Starboy that was released following in the same year. Needless to say, this data is only from Spotify, so we can only assume within the context of streaming data on Spotify. (References: Figure titled 'The Evolution of The Weeknd's Sounds', Table titled 'Summary of All Albums')")


st.markdown("---")

# # Get the unique album names from weekend_data
# album_names = weekend_data['album_name'].unique()

# # Create a Streamlit selectbox to choose an album
# selected_album = st.selectbox("Select an Album", album_names)

# # Filter the data for the selected album
# filtered_data = weekend_data[weekend_data['album_name'] == selected_album]

# # Create checkboxes to select which features to view
# audio_features = ['popularity', 'danceability', 'energy', 'tempo', 'valence']
# selected_features = st.multiselect("Select Audio Features to View", audio_features)

# # Create a Plotly Express scatterplot based on selected features
# st.header(f"Audio Features for Album: {selected_album}")
# fig = px.scatter(
#     filtered_data,
#     x="popularity",
#     y=selected_features,
#     labels={"popularity": "Popularity"},
#     title=f"Audio Features for Album: {selected_album}",
# )

# # Show the plot with selected features
# st.plotly_chart(fig)

st.markdown("---")

# Get the unique track names from weekend_data
track_names = weekend_data['track_name'].unique()

# Create a Streamlit selectbox to choose a track
selected_track = st.selectbox("Select a Track", track_names)

# Filter the data for the selected track
filtered_data = weekend_data[weekend_data['track_name'] == selected_track]

# Create checkboxes to select which features to view
# audio_features = ['popularity', 'danceability', 'energy', 'tempo', 'valence']
selected_features = st.multiselect("Select Audio Features to View", audio_features, default=audio_features)

# Create a Plotly Express scatterplot based on selected features
st.header(f"Audio Features for Track: {selected_track}")
fig = px.scatter(
    filtered_data,
    x="popularity",
    y=selected_features,
    labels={"popularity": "Popularity"},
    title=f"Audio Features for Track: {selected_track}",
)

# Show the plot with selected features
st.plotly_chart(fig)


st.markdown("---")

st.header('Conclusion')
st.write("Although every album has it's own characteristic style, whether it be a dark R&B themed House of Balloons or futuristic 80's themed Dawn FM, The Weeknd has successfully been able to create music with consistent mood and tempo that makes his sounds unique for the listeners: moody, mysterious and melancholy.")
