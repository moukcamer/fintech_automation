from sklearn.linear_model import LinearRegression
import numpy as np

def forecast_cashflow(monthly_df, periods=6):
    X = np.arange(len(monthly_df)).reshape(-1, 1)
    y = monthly_df["cashflow"].values

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(monthly_df), len(monthly_df) + periods).reshape(-1, 1)
    forecast = model.predict(future_X)

    return forecast.round(0)
