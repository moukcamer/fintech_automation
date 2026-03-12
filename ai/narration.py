def generate_narrative(kpis, risk, monthly_data, evolution_data, fraud_transactions):
    """
    Génère un résumé intelligent du dashboard
    """

    narrative = []

    # 1️⃣ Synthèse globale
    narrative.append(
        f"Le tableau de bord affiche {kpis['total_transactions']} transactions "
        f"avec un solde net de {kpis['net_balance']:,.0f} XAF."
    )

    # 2️⃣ Evolution mensuelle
    if monthly_data:
        trend = "croissante" if monthly_data[-1] > monthly_data[0] else "stable ou décroissante"
        narrative.append(
            f"L'évolution mensuelle semble {trend} sur la période analysée."
        )

    # 3️⃣ Evolution quotidienne
    if evolution_data:
        narrative.append(
            f"L'activité quotidienne montre {len(evolution_data)} jours d'activité."
        )

    # 4️⃣ Analyse du risque
    risk_score = risk.get("risk_score", 50)

    if risk_score < 25:
        level = "faible"
    elif risk_score < 60:
        level = "modéré"
    else:
        level = "élevé"

    narrative.append(f"Le score de risque est évalué à {risk_score}/100, niveau {level}.")

    alerts = risk.get("alerts", [])

    if alerts:
        narrative.append("Alertes détectées : " + "; ".join(alerts))
    else:
        narrative.append("Aucune anomalie majeure détectée.")

    return " ".join(narrative)

    # fraud transaction
    fraud_rate = 0
    if kpis["total_transactions"] > 0:
        fraud_rate = (fraud_transactions / kpis["total_transactions"]) * 100

    text = f"""
    Le système a détecté {fraud_transactions} transactions suspectes
    représentant {fraud_rate:.1f}% du volume total.

    Une surveillance renforcée est recommandée.
     """

    return text

