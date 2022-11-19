import warnings
import pandas as pd
import ast

warnings.filterwarnings("ignore")

from utils import coordinates_to_idx
from scipy import sparse
from tqdm import tqdm

df = pd.read_csv('data/statuses/preprocessed/train_data.csv')

df['waypoints'] = df['waypoints'].apply(lambda x: ast.literal_eval(x))
# df.timestamp_hour = df.timestamp_hour.str.zfill(2)

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
                sumy = [sum(weather_matrix[x - i, y - 5:y + 6]) for i in range(-5, 6, 1)]
                result_df.loc[0, f'waypoint_{id + 1}'] = sum(sumy)
        except:
            counter += 1
            continue
    print(counter)
    return result_df


new_df = estimate_weather_conditions_for_waypoints_in_timestamp(df)

new_df.to_csv("preprocessed_train.csv", index=False)
