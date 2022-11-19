import pandas as pd
from sklearn.model_selection import train_test_split

routes = pd.read_csv('data/statuses/route_definitions.csv')

train = pd.read_csv('data/statuses/train_observations.csv')
train_availability = pd.read_csv('data/statuses/train_availability.csv')

test_1000 = pd.read_csv('data/statuses/test_observations_1000.csv')
test = pd.read_csv('data/statuses/test_observations.csv')

# training data
df = pd.merge(train, train_availability, on="observation_id")
df = pd.merge(df, routes, on='route_id')
df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0])
df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:8])

train_data, val = train_test_split(df, train_size=.8, stratify=df['status'])
train_data.to_csv('data/statuses/train_data.csv', index=False)
val.to_csv('data/statuses/val_data.csv', index=False)


# test data
df = pd.merge(test, routes, on='route_id')
df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0])
df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:8])
df.to_csv('data/statuses/test.csv', index=False)

# test 1000 data
df = pd.merge(test_1000, routes, on='route_id')
df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0])
df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:8])
df.to_csv('data/statuses/test_1000.csv', index=False)
