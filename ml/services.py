#ml/services.py

import numpy as np
from sklearn.linear_model import LinearRegression
from django.conf import settings
import os
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

def detect_fraud(transaction):
    try:
        # simulation modèle IA
        result = {
            "fraud_probability": 0.12,
            "is_fraud": False,
            "status": "OK"
        }

        return result

    except Exception as e:
        return {
            "fraud_probability": 0.0,
            "is_fraud": False,
            "status": f"ERROR: {str(e)}"
        }




def apply_fraud_result(transaction, result):

    # sécurité : enlever espaces dans clés
    result = {k.strip(): v for k, v in result.items()}

    transaction.is_fraud = bool(result.get("is_fraud", False))
    transaction.fraud_probability = float(result.get("fraud_probability", 0.0))
    transaction.ai_status = result.get("status", "OK")

    # stocker tout le rapport IA
    transaction.fraud_analysis = result

    transaction.save()