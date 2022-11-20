import numpy as np
import pandas as pd
from typing import List, Tuple
from datetime import datetime
import math
import ast

class Preprocessor:
    def __init__(self, df) -> None:
        self.df = df

    def preprocess_train(self) -> pd.DataFrame:
            self._encode_status()
            self._encode_route_type()
            # self._one_hot_encode_airports()
            self._apply_feature_engineering()
            self._extract_info_from_date()
            self._drop_irrelevant_features(['waypoints', 'timestamp', 'route_id', 'timestamp_date', 'observation_id'])
            # self._drop_irrelevant_features([f'waypoint_{idx}' for idx in range(1, 21)])
            return self.df

    def preprocess_test(self) -> pd.DataFrame:
            self._encode_route_type()
            # self._one_hot_encode_airports()
            self._apply_feature_engineering()
            self._extract_info_from_date()
            self._drop_irrelevant_features(['waypoints', 'timestamp', 'route_id', 'timestamp_date'])
            # self._drop_irrelevant_features([f'waypoint_{idx}' for idx in range(1, 21)])
            return self.df
            
    def _encode_status(self) -> None:
        self.df['status'] = np.where(self.df['status'] == "OPEN", 1, 0)
    
    def _encode_route_type(self) -> None:
        self.df['route_type'] = np.where(self.df['route_type'] == 'ARRIVAL', 1, 0)
    
    # def _one_hot_encode_airports(self) -> None:
    #     one_hot = pd.get_dummies(self.df['airport'])
    #     self.df.drop('airport', axis = 1, inplace=True)
    #     self.df = self.df.join(one_hot)

    def _apply_feature_engineering(self) -> None:
        self.df['distance'] = self.df['waypoints'].apply(lambda x: self.distance_fromlist(eval(x)))
        self.df['no_of_waypoints'] = self.df['waypoints'].apply(lambda x: len(eval(x)))
        self.df['dayoftheweek'] = pd.to_datetime(self.df['timestamp_date']).dt.dayofweek
        
        self.df['waypoints'] = self.df['waypoints'].apply(lambda x: ast.literal_eval(x))
        self.df['north'] = np.where((self.df['route_type']== 0) & (self.df.waypoints.apply(lambda x: x[1][0] - x[0][0]) >= 0), 1,
                            np.where((self.df['route_type']==1) & (self.df.waypoints.apply(lambda x: x[-1][0] - x[-2][0]) >= 0),1,0))
        self.df['west'] =  np.where((self.df['route_type']==0) & (self.df.waypoints.apply(lambda x: x[1][1] - x[0][1]) >= 0), 1,
                            np.where((self.df['route_type']==1) & (self.df.waypoints.apply(lambda x: x[-1][1] - x[-2][1]) >= 0),1,0))

    def _extract_info_from_date(self) -> None:
        self.df['timestamp_month'] = self.df['timestamp_date'].astype(str).str[8:10].astype(int)
        self.df['timestamp_day'] = self.df['timestamp_date'].astype(str).str[5:7].astype(int)
        self.df['timestamp_hour'] = self.df['timestamp_hour'].astype(str).str[:2].astype(int)

    def _drop_irrelevant_features(self, features: List[str]) -> None:
        self.df.drop(features, axis=1, inplace=True)

    def distance(self, coords_1: Tuple[float, float], coords_2: Tuple[float, float]) -> int:
        return math.sqrt((coords_1[0] - coords_2[0]) ** 2 + (coords_1[1] - coords_2[1]) ** 2)

    def distance_fromlist(self, lst: List[Tuple[int, int]]) -> int:
        all_distance = 0
        for i in range(len(lst) - 1):
            all_distance += self.distance(lst[i], lst[i + 1])
        return all_distance


        