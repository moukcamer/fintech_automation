import pandas as pd

def compute_client_score(df):
    """
    Calcul du score financier client (0-100)
    """

    if df.empty:
        return {"score": 50, "level": "Neutre"}

    total_transactions = len(df)
    total_credit = df[df["amount"] > 0]["amount"].sum()
    total_debit = abs(df[df["amount"] < 0]["amount"].sum())

    balance = total_credit - total_debit

    # ratio crédit/débit
    if total_debit == 0:
        ratio = 1
    else:
        ratio = total_credit / total_debit

    score = 50

    # activité
    if total_transactions > 100:
        score += 10
    elif total_transactions < 10:
        score -= 10

    # ratio financier
    if ratio > 1.2:
        score += 20
    elif ratio < 0.8:
        score -= 20

    # solde
    if balance > 0:
        score += 10
    else:
        score -= 10

    score = max(0, min(100, score))

    if score >= 80:
        level = "Client fiable"
    elif score >= 60:
        level = "Client normal"
    elif score >= 40:
        level = "Client à surveiller"
    else:
        level = "Client risqué"

    return {
        "score": score,
        "level": level
    }
