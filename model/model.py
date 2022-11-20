import pandas as pd
from xgboost import XGBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from typing import Tuple

class Model:

    def __init__(self) -> None:
        self.model = XGBoostClassifier()
    
    def model_train_test_split(self, X: pd.DataFrame, y: pd.DataFrame, test_size: float = 0.2, random_state: int = 420) -> Tuple[pd.DataFrame,pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        train_test_split(X, y, test_size, random_state)

    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> None:
        self.model.fit(X_train, y_train)
    
    def predict(self, X_test: pd.DataFrame) -> pd.Series:
        return self.model.predict(X_test)

    def calculate_f1(self, y_pred: pd.Series, y_test: pd.Series) -> int:
        f1 = f1_score(y_test, y_pred)
        print(f"f1_score: {f1}")
        return f1


