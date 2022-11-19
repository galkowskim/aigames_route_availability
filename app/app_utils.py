from sklearn.ensemble import RandomForestClassifier
from math import sqrt
from pathlib import Path
import pandas as pd
import folium

def make_map(points, result):
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


def validate(df, id_route):
    return