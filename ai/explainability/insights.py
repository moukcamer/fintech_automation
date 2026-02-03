def explain_forecast(history, forecast):
    trend = "hausse" if forecast[-1] > history[-1] else "baisse"

    return {
        "trend": trend,
        "main_driver": "entrées" if trend == "hausse" else "sorties",
        "confidence": "élevée" if abs(forecast[-1] - history[-1]) < 0.15 * history[-1] else "modérée"
    }

def compute_risk_score(net_result, cash_balance, volatility):
    score = 0

    if net_result < 0:
        score += 40

    if cash_balance < abs(net_result):
        score += 30

    if volatility > 0.25:
        score += 30

    return min(score, 100)
