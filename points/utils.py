import folium
import numpy as np
from scipy import sparse
from math import sqrt

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


def plot_matrix(sparse_matrix: sparse.csr_matrix, points) -> folium.Map:
    fmap = folium.Map(location=[35, -100], zoom_start=6)

    colored_matrix = matrix_to_weather_colormap(sparse_matrix=sparse_matrix)

    folium.raster_layers.ImageOverlay(
        colored_matrix,
        pixelated=True,
        opacity=0.8,
        mercator_project=True,
        bounds=BOUNDARIES,
    ).add_to(fmap)

    # add points list to folium map
    for point in points:
        folium.CircleMarker(location=(point[0], point[1]),
                            radius=2,
                            weight=5).add_to(fmap)
    return fmap


def load_and_show_vil(file_path: str, points) -> folium.Map:
    sparse_matrix = sparse.load_npz(file_path)
    plot = plot_matrix(sparse_matrix=sparse_matrix, points=points)
    return plot


def distance(coords_1, coords_2):
    return sqrt((coords_1[0] - coords_2[0]) ** 2 + (coords_1[1] - coords_2[1]) ** 2)


def get_route(coords_1, coords_2, n):
    return [(coords_1[0] + (coords_2[0] - coords_1[0]) * i / n, coords_1[1] + (coords_2[1] - coords_1[1]) * i / n) for i
            in range(n)]


def all_routes(lst, c=500):
    all_points = []
    if c < len(lst):
        c = len(lst)

    distance_list = list()
    all_distance = 0
    for i in range(len(lst) - 1):
        distance_list.append(distance(lst[i], lst[i + 1]))
        all_distance += distance(lst[i], lst[i + 1])

    for i in range(len(lst) - 2):
        n = round(int(c * distance_list[i] / all_distance))
        if n == 0:
            n = 1
        all_points += get_route(lst[i], lst[i + 1], n)

    how_many_left = c - len(all_points)
    all_points += get_route(lst[-2], lst[-1], how_many_left - 1)
    all_points.append(lst[-1])
    return all_points


def make_map(path, points, c=500):
    return load_and_show_vil(path,
                             points=all_routes(points, c))
