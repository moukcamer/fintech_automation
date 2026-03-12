def auto_financial_insight(kpis, monthly_data, type_data, risk):

    insights = []

    # analyse solde
    if kpis["net_balance"] > 0:
        insights.append(
            "La plateforme génère un solde financier positif."
        )
    else:
        insights.append(
            "Attention : le solde net est négatif."
        )

    # analyse tendance
    if len(monthly_data) > 1:

        if monthly_data[-1] > monthly_data[-2]:
            insights.append(
                "Les revenus mensuels sont en croissance."
            )
        else:
            insights.append(
                "Une baisse de performance est observée ce mois."
            )

    # analyse type transaction
    if len(type_data) >= 2:

        if abs(type_data[1]) > type_data[0]:
            insights.append(
                "Les dépenses dépassent les revenus."
            )
        else:
            insights.append(
                "Les revenus couvrent les dépenses."
            )

    # analyse fraude
    score = risk.get("risk_score", 50)

    if score > 70:
        insights.append(
            "Risque de fraude élevé détecté."
        )
    elif score > 40:
        insights.append(
            "Risque financier modéré."
        )
    else:
        insights.append(
            "Aucun risque majeur détecté."
        )

    return insights
