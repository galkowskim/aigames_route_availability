import math
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy import sparse

from typing import Tuple
# (21.9430, -67.5), (55.7765, -135)
# difference on each coordinate (33.8335, 67.5)
# shape 2566x5120

# Longitude mapping
# 21.9430 - 0
# 55.7765 - 2565

# Latitude mapping
# -135  -  0
# -67.5 - 5119

BOUNDARIES = [(21.9430, -67.5), (55.7765, -135)]
delta_latitude = BOUNDARIES[1][0] - BOUNDARIES[0][0]
delta_longitude = BOUNDARIES[1][1] - BOUNDARIES[0][1]

shape = (2565, 5119)  # 2566, 5120


def coordinates_to_idx(latitude: int, longitude: int) -> Tuple[int]:
    prop_latitude = (latitude - BOUNDARIES[0][0]) / delta_latitude
    prop_longitude = (longitude - BOUNDARIES[0][1]) / delta_longitude

    x = shape[0] - math.floor(prop_latitude * shape[0])
    y = shape[1] - math.floor(prop_longitude * shape[1])

    return x, y


NUMBER_OF_WAYPOINTS = 15
colnames = [f"waypoint_{i + 1}" for i in range(NUMBER_OF_WAYPOINTS)]

def estimate_weather_conditions_for_waypoints_in_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    result_df = df.copy()
    counter = 0
    for col in colnames:
        result_df[col] = 0
    for idx, row in tqdm(df.iterrows()):
        try:
            file = f'data/VIL_merc/VIL-{row.loc["timestamp_date"]}-{row.loc["timestamp_hour"]}_00Z.npz'
            weather_matrix = sparse.load_npz(file).toarray()
            result_df.iloc[idx][df.columns] = df.iloc[idx]

            for id, waypoint in enumerate(row['waypoints']):
                x, y = coordinates_to_idx(waypoint[0], waypoint[1])
                sumy = [np.mean(weather_matrix[x - i, y - 5:y + 6]) for i in range(-2, 3, 1)]
                result_df.loc[0, f'waypoint_{id + 1}'] = np.mean(sumy)
        except:
            counter += 1
            continue
    print(counter)
    return result_df