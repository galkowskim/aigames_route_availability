import math
from typing import Tuple
# (21.9430, -67.5), (55.7765, -135)
# (33.8335, 67.5)
# shape 2566x5120

# 21.9430 - 0           55.7765 - 2565

# -67.5 - 0             -135  -  5119

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
