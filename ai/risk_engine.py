# ai/risk_engine.py
import numpy as np

def compute_risk(df):
    if df.empty:
        return {"risk_score": 0, "alerts": []}

    alerts = []

    # transactions très élevées
    high_amount = df["amount"].mean() * 5
    suspicious = df[df["amount"] > high_amount]

    if len(suspicious) > 0:
        alerts.append(f"{len(suspicious)} transactions anormalement élevées détectées")

    # trop de débits
    debit_ratio = df["is_debit"].mean()
    if debit_ratio > 0.8:
        alerts.append("Trop de sorties d'argent — risque de fuite financière")

    # score final
    score = min(100, int((len(alerts) * 25) + debit_ratio * 50))

    return {
        "risk_score": score,
        "alerts": alerts
    }

