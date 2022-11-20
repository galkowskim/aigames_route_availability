from scipy import sparse
from sklearn.ensemble import RandomForestClassifier
from math import sqrt
from pathlib import Path
import pandas as pd
import folium
import streamlit as st
import numpy as np

BOUNDARIES = [(21.9430, -67.5), (55.7765, -135)]
VIL_THRESHOLD_COLORS = [
    (10000, (0.63, 0.0, 0.01, 1.0)),
    (32.32, (0.87, 0.56, 0.0, 1.0)),
    (12.16, (0.95, 0.75, 0.0, 1.0)),
    (7.08, (0.93, 0.95, 0.0, 1.0)),
    (3.53, (0.38, 0.69, 0.0, 1.0)),
    (0.77, (0.63, 0.94, 0.0, 1.0)),
    (0.52, (0.9, 0.9, 0.9, 0.03)),
]


def matrix_to_weather_colormap(sparse_matrix: sparse.csr_matrix) -> np.ndarray:
    matrix = sparse_matrix.toarray()
    result = np.zeros(shape=matrix.shape + (4,))
    for thresh, color in VIL_THRESHOLD_COLORS:
        result[matrix <= thresh] = color
    return result


def make_map(points, result, date, time):
    date = str(date)
    time = str(time)
    date = date[:5] + date[8:10] + date[4] + date[5:7]
    time = time[:2]

    color = 'green' if result else 'red'
    fmap = folium.Map(location=[points[0][0], points[0][1]], zoom_start=11)
    for i in range(1, len(points)):
        folium.PolyLine([[points[i - 1][0], points[i - 1][1]],
                         [points[i][0], points[i][1]]],
                        color=color).add_to(fmap)
    for i in range(len(points)):
        folium.CircleMarker(location=(points[i][0], points[i][1]),
                            radius=2,
                            weight=5,
                            color=color).add_to(fmap)

    try:
        matrix = load_weather_data(date, time)
        colored_matrix = matrix_to_weather_colormap(sparse_matrix=matrix)

        folium.raster_layers.ImageOverlay(
            colored_matrix,
            pixelated=True,
            opacity=0.8,
            mercator_project=True,
            bounds=BOUNDARIES,
        ).add_to(fmap)
    except:
        st.markdown('No weather data for this day and time.')

    return fmap

def distance(coords_1, coords_2):
    return sqrt((coords_1[0] - coords_2[0]) ** 2 + (coords_1[1] - coords_2[1]) ** 2)


def get_route(coords_1, coords_2, n):
    return [(coords_1[0] + (coords_2[0] - coords_1[0]) * i / n, coords_1[1] + (coords_2[1] - coords_1[1]) * i / n) for i
            in range(n)]


def get_all_points(points, c=50):
    all_points = []
    if c < len(points):
        c = len(points)

    distance_list = list()
    all_distance = 0
    for i in range(len(points) - 1):
        distance_list.append(distance(points[i], points[i + 1]))
        all_distance += distance(points[i], points[i + 1])

    for i in range(len(points) - 2):
        n = round(int(c * distance_list[i] / all_distance))
        if n == 0:
            n = 1
        all_points += get_route(points[i], points[i + 1], n)

    how_many_left = c - len(all_points)
    all_points += get_route(points[-2], points[-1], how_many_left - 1)
    all_points.append(points[-1])
    return all_points


def load_model():
    return RandomForestClassifier()


def load_data():
    file_path = Path(__file__).resolve()
    data_path = file_path.parents[1].joinpath('data', 'statuses', 'route_definitions.csv')
    return pd.read_csv(data_path)

def load_weather_data(date, time):
    file_path = Path(__file__).resolve()
    data_path = file_path.parents[1].joinpath('data', 'VIL_merc', f'VIL-{date}-{time}_00Z.npz')
    matrix = sparse.load_npz(data_path)
    return matrix

def validate(df, id_route):
    return