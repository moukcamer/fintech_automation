#ml/services.py

import numpy as np
from sklearn.linear_model import LinearRegression

from .utils import get_monthly_payments_df


def forecast_payments(months_ahead=6):
    df = get_monthly_payments_df()

    if df.empty or len(df) < 3:
        return []

    # Feature engineering
    df["t"] = range(len(df))

    X = df[["t"]]
    y = df["amount"]

    model = LinearRegression()
    model.fit(X, y)

    future = []
    last_t = df["t"].iloc[-1]

    for i in range(1, months_ahead + 1):
        t_future = np.array([[last_t + i]])
        amount_pred = model.predict(t_future)[0]

        future.append({
            "month": i,
            "predicted_amount": round(max(amount_pred, 0), 2)
        })

    return future

import joblib
import pandas as pd

MODEL_PATH = "ml/fraud_model.pkl"


def detect_fraud(transaction):

    model = joblib.load(MODEL_PATH)

    data = pd.DataFrame([{
        "amount": transaction.amount,
        "transaction_type": 1 if transaction.transaction_type == "IN" else 0,
        "country": transaction.country
    }])

    pred = model.predict(data)[0]

    return pred == -1



