import pandas as pd
import numpy as np

def detect_anomalies(df):

    alerts = []
    df = df.sort_values("date")

    for account in df["account_number"].unique():

        acc = df[df["account_number"] == account]

        if len(acc) < 5:
            continue

        mean = acc["amount"].mean()
        std = acc["amount"].std()

        if std == 0:
            continue

        threshold_high = mean + 3*std
        threshold_low = mean - 3*std

        for _, row in acc.iterrows():

            if row["amount"] > threshold_high:
                alerts.append({
                    "account": account,
                    "date": row["date"],
                    "amount": row["amount"],
                    "type": "SPIKE",
                    "message": "Montant anormalement élevé"
                })

            if row["amount"] < threshold_low:
                alerts.append({
                    "account": account,
                    "date": row["date"],
                    "amount": row["amount"],
                    "type": "ABNORMAL_LOW",
                    "message": "Montant anormalement faible"
                })

    return alerts

def detect_frequency_fraud(df):

    alerts = []

    df["date"] = pd.to_datetime(df["date"])
    grouped = df.groupby("account_number")

    for acc, data in grouped:

        daily_counts = data.groupby(data["date"].dt.date).size()

        if daily_counts.max() > daily_counts.mean()*4:
            alerts.append({
                "account": acc,
                "type": "FREQUENCY",
                "message": "Trop de transactions sur une journée"
            })

    return alerts

