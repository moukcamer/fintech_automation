import random

def calculate_risk(transaction):

    score = 0

    # Montant élevé
    if transaction.amount > 500000:
        score += 40

    # Localisation suspecte
    suspicious_countries = ["Russia", "China", "Unknown"]
    if transaction.location in suspicious_countries:
        score += 30

    # Nuit profonde
    if transaction.timestamp.hour < 5:
        score += 15

    # Device inconnu
    if "bot" in transaction.device.lower():
        score += 20

    return min(score, 100)

def classify(score):
    if score < 30:
        return "normal"
    elif score < 70:
        return "suspect"
    return "fraud"


def check_fraud(transaction=None, amount=None):

    if transaction:
        amount = transaction.amount

    if amount is None:
        return {
            "risk_score": 0,
            "is_fraud": False,
            "status": "ERROR"
        }

    if amount > 1000000:
        risk_score = 85
    elif amount > 500000:
        risk_score = 60
    else:
        risk_score = 10

    return {
        "risk_score": risk_score,
        "is_fraud": risk_score >= 80,
        "status": "OK"
    }
