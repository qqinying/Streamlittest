import streamlit as st
import pandas as pd
import numpy as np

# set page
st.set_page_config(
     page_title="CCS App",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.google.com',
         'Report a bug': "https://www.github.com",
         'About': "# This is a CCS app. This is an *extremely* cool app!"
     }
 )

# app title
st.title("Uber pickups in NYC by JY (beta version)")

# fetch data
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Cache the data
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10000 rows of data into the dataframe
data = load_data(10000)
# Notify the reader that the data was successfully loaded
# data_load_state = st.text('Loading data...done!')
data_load_state.text("Done! (using st.cache)")

# Inspect the raw data
# st.subheader('Raw data')
# st.write(data)

# Draw histogram by Numpy
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Plot data on a map
st.subheader('Map of all pickups')
st.map(data)

# Filter data
# hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)
filter_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filter_data)

# Use a button to toggle data
if st.checkbox('Show raw data'):
    st.subheader('Raw data(filtered by hours)')
    st.write(filter_data)



