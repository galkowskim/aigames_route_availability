import ast
import streamlit as st
from app.app_utils import load_model, make_map, load_data, validate, get_all_points
import numpy as np
from streamlit_folium import folium_static

def run():
    st.title("VIL map")
    id_route = st.text_input("Route id")
    date = st.date_input("Date")
    time = st.time_input("Time")
    button = st.button("Submit")
    try:
        model = load_model()
        df = load_data()
    except FileNotFoundError:
        st.error("No data available (error 500 :D)")

    if button:
        validate(df, id_route)
        # result = model.predict(np.array(id_route, date, time))
        # st.write(result)

        route = [ast.literal_eval(el) for el in df.loc[df['route_id'] == id_route]['waypoints']][0]
        map = make_map(route, 1)

        st.markdown(f"Route: {id_route}")
        folium_static(map)