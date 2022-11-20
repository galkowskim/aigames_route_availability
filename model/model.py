import pandas as pd
import lightgbm
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from typing import Tuple
from sklearn.preprocessing import OneHotEncoder

class Model:

    def __init__(self) -> None:
        # self.model = xgboost.XGBClassifier()
        self.model = lightgbm.LGBMClassifier()
        self.ohe = OneHotEncoder()
        self.col = None

    def model_train_test_split(self, X: pd.DataFrame, y: pd.DataFrame, test_size: float = 0.2, random_state: int = 420) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
        return train_test_split(X, y, test_size, random_state)

    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
        index = X_train.index
        drop = X_train.drop(['airport'], axis=1)
        X_train = self.ohe.fit_transform(X_train[['airport']]).toarray()
        self.col = self.ohe.get_feature_names_out(['airport'])
        X_train = pd.DataFrame(X_train, columns=self.col, index=index)
        X_train = X_train.join(drop)

        print(X_train.columns)
        print(len(X_train.columns))
        self.model.fit(X_train, y_train)
    
    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        obs = X_test[['observation_id']]
        X_test = X_test.drop('observation_id', axis=1)
        results = pd.Series(self.model.predict(X_test))
        print(results)
        obs['results'] = results
        obs.to_csv('results.csv', index=False)
        return obs
        

    def onehot(self, X_test):
        index = X_test.index
        drop = X_test.drop(['airport'], axis=1)
        X_test = self.ohe.transform(X_test[['airport']]).toarray()
        
        X_test = pd.DataFrame(X_test, columns=self.col, index=index)
        X_test = X_test.join(drop)
        return X_test

    def calculate_f1(self, y_pred: pd.Series, y_test: pd.Series) -> int:
        f1 = f1_score(y_test, y_pred)
        print(f"f1_score test: {f1}")
        return f1


