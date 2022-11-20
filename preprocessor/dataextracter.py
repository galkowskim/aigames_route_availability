from pathlib import Path
import pandas as pd
import os

class DataExtracter:
    def __init__(self):
        self.path = Path(__file__).resolve()

    def extract_data(self):
        test = pd.read_csv(self.path.parent.parent / 'data' / 'statuses' / 'test_observations.csv')
        print(self.path.parent.parent / 'data' / 'statuses' / 'test_observations.csv')
        routes = pd.read_csv(self.path.parent.parent / 'data' / 'statuses' / 'route_definitions.csv')
        self.merge(test, routes)

    def merge(self, test, routes):
        df = pd.merge(test, routes, on='route_id')
        df['timestamp_date'] = df.timestamp.str.split(' ').apply(
            lambda row: row[0][:5] + row[0][8:10] + row[0][7] + row[0][5:7])
        df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:2])
        return df

    
    def train(self):
        routes = pd.read_csv(os.path.join(self.path.parent.parent, 'data','statuses','route_definitions.csv'))
        train = pd.read_csv(os.path.join(self.path.parent.parent, 'data','statuses', 'train_observations.csv'))
        train_availability = pd.read_csv(os.path.join(self.path.parent.parent, 'data','statuses', 'train_availability.csv'))
        df = pd.merge(train, train_availability, on="observation_id")
        df = pd.merge(df, routes, on='route_id')
        df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0][:5] + row[0][5:7] + row[0][7] + row[0][8:10])
        df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:2])
        return df
    
    def test(self):
        routes = pd.read_csv(os.path.join(self.path.parent.parent, 'data','statuses','route_definitions.csv'))
        test = pd.read_csv(os.path.join(self.path.parent.parent, 'data','statuses', 'test_observations.csv'))
        df = pd.merge(test, routes, on='route_id')
        # df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0][:5] + row[0][8:10] + row[0][7] + row[0][5:7])
        df['timestamp_date'] = df.timestamp.str.split(' ').apply(lambda row: row[0][:5] + row[0][5:7] + row[0][7] + row[0][8:10])
        df['timestamp_hour'] = df.timestamp.str.split(' ').apply(lambda row: row[1][:2])
        return df

    def load(self, name):

        return pd.read_csv(path)