# app.py
import pandas as pd
import streamlit as st
import pydeck as pdk
import plotly.express as px
import numpy as np

max_threshold = 1000

def get_gradient_color(crime_count, threshold):
    """
    Returns [R, G, B] color for a crime count relative to the threshold.
    Green = below threshold, Red = above threshold, Yellow = at threshold.
    """
    if crime_count <= threshold:
        # Gradient from green (0,255,0) to yellow (255,255,0)
        ratio = crime_count / threshold
        r = int(255 * ratio)
        g = 255
    else:
        # Gradient from yellow (255,255,0) to red (255,0,0)
        ratio = min((crime_count - threshold) / threshold, 1.0)
        r = 255
        g = int(255 * (1 - ratio))
    b = 0
    return [r, g, b]

# ---- Load CSV ----
# Replace with your actual CSV path
df = pd.read_csv("merged_output.csv")

# ---- Filter for London Zone 2 ----
# Approximate bounding box for London Zone 2
# (min_lon, max_lon, min_lat, max_lat)
zone2_bbox = [-0.34, 0.05, 51.4, 51.6]

df_london = df[
    (df['Longitude'] >= zone2_bbox[0]) & (df['Longitude'] <= zone2_bbox[1]) &
    (df['Latitude'] >= zone2_bbox[2]) & (df['Latitude'] <= zone2_bbox[3])
].copy()

# ---- Aggregate total crimes by LSOA ----
lsoa_agg = df_london.groupby('LSOA name').agg(
    TotalCrimes=('Crime ID', 'count'),
    Latitude=('Latitude', 'mean'),
    Longitude=('Longitude', 'mean')
).reset_index()

sorted_crimes = np.sort(lsoa_agg['TotalCrimes'])
cdf = np.arange(1, len(sorted_crimes)+1) / len(sorted_crimes)

fig = px.line(
    x=sorted_crimes,
    y=cdf,
    labels={'x': 'Total Crimes', 'y': 'CDF'},
    title='CDF of Total Crimes per LSOA'
)
fig.update_xaxes(range=[0, max_threshold])
st.plotly_chart(fig, use_container_width=True)

# ---- Streamlit interface ----
st.set_page_config(layout="wide")
st.title("London Zone 2 Crime Map")

threshold = st.slider("Crime threshold", min_value=0, max_value=max_threshold, value=190)

# Determine dot colors based on threshold
lsoa_agg['color'] = lsoa_agg['TotalCrimes'].apply(lambda x: get_gradient_color(x, threshold))

# ---- PyDeck Map ----
layer = pdk.Layer(
    "ScatterplotLayer",
    data=lsoa_agg,
    get_position='[Longitude, Latitude]',
    get_fill_color='color',
    get_radius=35,
    pickable=True,
)

# Tooltip shows LSOA name and total crimes
tooltip = {"html": "<b>{LSOA name}</b><br>Total Crimes: {TotalCrimes}", "style": {"color": "white"}}

view_state = pdk.ViewState(
    latitude=51.515,
    longitude=-0.07,
    zoom=12,
    pitch=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style='road'
)

st.pydeck_chart(r)
