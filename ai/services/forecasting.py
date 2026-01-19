import pandas as pd
from sklearn.linear_model import LinearRegression

class FinancialForecastService:

    def __init__(self):
        self.model = LinearRegression()

    def train(self, df, target):
        X = df.drop(columns=[target])
        y = df[target]
        self.model.fit(X, y)

    def predict(self, future_df):
        return self.model.predict(future_df)
