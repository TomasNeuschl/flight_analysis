import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

flight_id = st.query_params.get('flight_id')

telemetry_data = requests.get(f'http://127.0.0.1:8000/api/v1/flight/{flight_id}/telemetry/')
status_data = requests.get(f'http://127.0.0.1:8000/api/v1/flight/{flight_id}/status/')

data = [{
    "color": [255, 0, 0],
    "path": telemetry_data.json()['path']
}]
df = pd.DataFrame(data)

layer = pdk.Layer(
    type='PathLayer',
    data=df,
    pickable=True,
    get_color='color',
    width_scale=20,
    width_min_pixels=2,
    get_path='path',
    get_width=0.005
)

view_state = pdk.ViewState(
    latitude=df['path'][0][0][1],
    longitude=df['path'][0][0][0],
    zoom=12,
)

deck = pdk.Deck(
    initial_view_state=view_state,
    layers=[layer],
)

st.pydeck_chart(deck)
