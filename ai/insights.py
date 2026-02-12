# ai/insights.py
def generate_insight(kpis, risk):

    if risk["risk_score"] < 25:
        level = "🟢 Situation financière saine"
    elif risk["risk_score"] < 60:
        level = "🟡 Surveillance recommandée"
    else:
        level = "🔴 Risque financier élevé"

    message = f"""
Analyse automatique :

{level}

Solde net : {kpis['net_balance']:,.0f}
Transactions : {kpis['total_transactions']}

Observations :
"""

    for a in risk["alerts"]:
        message += f"- {a}\n"

    if not risk["alerts"]:
        message += "- Aucun comportement anormal détecté"

    return message
