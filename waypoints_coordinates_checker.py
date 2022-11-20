import ast
import pandas as pd

max_long = -300
min_long = 500

max_lat = -300
min_lat = 500

df = pd.read_csv('data/statuses/preprocessed/train_data.csv')

for el in df.waypoints.apply(lambda x: ast.literal_eval(x)):
    for tmp in el:
        if tmp[0] > max_lat:
            max_lat = tmp[0]
        if tmp[0] < min_lat:
            min_lat = tmp[0]
        if tmp[1] > max_long:
            max_long = tmp[1]
        if tmp[1] < min_long:
            min_long = tmp[1]

print(f"max longitude: {max_long}, min latitude: {min_long}")
print(f"max latitude: {max_lat}, min latitude: {min_lat}")
