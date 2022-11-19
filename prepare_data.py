import pandas as pd

routes = pd.read_csv('data/statuses/route_definitions.csv')

train = pd.read_csv('data/statuses/train_observations.csv')
train_availability = pd.read_csv('data/statuses/train_availability.csv')

test_1000 = pd.read_csv('data/statuses/test_observations_1000.csv')
test = pd.read_csv('data/statuses/test_observations.csv')

df = pd.merge(train, train_availability, on="observation_id")
df = pd.merge(df, routes, on='route_id')
df.to_csv('data/statuses/train_data.csv', index=False)

