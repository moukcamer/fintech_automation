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