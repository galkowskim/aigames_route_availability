import pandas as pd
import os
import shutil
from sklearn.model_selection import train_test_split

PATH_TO_DATA = 'data/statuses/'
PATH_TO_SAVE = 'data/statuses/preprocessed/'

if not os.path.exists(PATH_TO_SAVE):
    os.makedirs(PATH_TO_SAVE)
else:
    for filename in os.listdir(PATH_TO_SAVE):
        file_path = os.path.join(PATH_TO_SAVE, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

routes = pd.read_csv(os.path.join(PATH_TO_DATA, 'route_definitions.csv'))

train = pd.read_csv(os.path.join(PATH_TO_DATA, 'train_observations.csv'))
train_availability = pd.read_csv(os.path.join(PATH_TO_DATA, 'train_availability.csv'))

test = pd.read_csv(os.path.join(PATH_TO_DATA, 'test_observations.csv'))

# training data
df = pd.merge(train, train_availability, on="observation_id")
df = pd.merge(df, routes, on='route_id')
df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0][:5] + row[0][8:10] + row[0][7] + row[0][5:7])
df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:2])

train_data, val = train_test_split(df, train_size=.8, stratify=df['status'])
train_data.to_csv(os.path.join(PATH_TO_SAVE, 'train_data.csv'), index=False)
val.to_csv(os.path.join(PATH_TO_SAVE, 'val_data.csv'), index=False)


# test data
df = pd.merge(test, routes, on='route_id')
df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0][:5] + row[0][8:10] + row[0][7] + row[0][5:7])
df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:2])
df.to_csv(os.path.join(PATH_TO_SAVE, 'test.csv'), index=False)


