import streamlit as st
import pydeck as pdk
import pandas as pd

# stationFrame = pd.read_excel('stationData.xlsx')
stationFrame = pd.read_csv('stationData.csv')

layer = pdk.Layer(
    'HexagonLayer',  
    stationFrame,
    get_position=['Longitude', 'Latitude'],
    auto_highlight=True,
    radius=7000,
    extruded=True,
    pickable=True,
)

# Set the viewport location
view_state = pdk.ViewState(
    longitude=36, latitude=40, zoom=4.5
)
# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[layer],
    tooltip={
            "html": "<b>Istasyon:</b> {ID}",
            "style": {"color": "white"},
        },
    
)
st.pydeck_chart(r)