import warnings
import pandas as pd
import ast
import numpy as np

warnings.filterwarnings("ignore")

from utils import coordinates_to_idx, estimate_weather_conditions_for_waypoints_in_timestamp
from scipy import sparse
from tqdm import tqdm

df = pd.read_csv('data/statuses/preprocessed/train_data.csv')

df['waypoints'] = df['waypoints'].apply(lambda x: ast.literal_eval(x))
df.timestamp_hour = df.timestamp_hour.astype(str)
df.timestamp_hour = df.timestamp_hour.str.zfill(2)

NUMBER_OF_WAYPOINTS = 20
colnames = [f"waypoint_{i + 1}" for i in range(NUMBER_OF_WAYPOINTS)]

new_df = estimate_weather_conditions_for_waypoints_in_timestamp(df)

new_df.to_csv("preprocessed_train.csv", index=False)
