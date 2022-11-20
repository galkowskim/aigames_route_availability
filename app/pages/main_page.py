import ast
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from streamlit_folium import folium_static
from app.app_utils import load_model, make_map, load_data, validate, get_all_points
from preprocessor.preprocessor import Preprocessor

def run():
    st.markdown("Detect whether you flight is available")
    id_route = st.text_input("Route id")
    date = st.date_input("Date", value=datetime.date(2020, 1, 1))
    time = st.time_input("Time", value=datetime.time(0, 00))
    button = st.button("Submit")
    try:
        model = load_model()
        df = load_data()
    except FileNotFoundError:
        st.error("No data available (error 500 :D)")

    if button:
        if not validate(df, id_route):
            st.markdown(f"Route ({id_route}) not in our data.")
        else:
            df = pd.DataFrame.from_dict({"route_id": [id_route], "timestamp_date": [date], "timestamp_hour": [time]})

            processor = Preprocessor(df)
            preprocessed = processor.preprocess_sample()
            preprocessed = model.onehot(preprocessed)

            result = model.predict_sample(preprocessed)
            pred_class = 'OPEN' if result[0] == 1 else 'CLOSED'
            st.markdown(f"Predicted class: **{pred_class}**")

            df = pd.DataFrame.from_dict({"route_id": [id_route], "timestamp_date": [date], "timestamp_hour": [time]})

            processor = Preprocessor(df)
            df_all_cols = processor.preprocess_sample_dont_drop_col()

            route = [el for el in df_all_cols.loc[df['route_id'] == id_route]['waypoints']][0]
            map = make_map(route, result[0], date, time)

            folium_static(map)