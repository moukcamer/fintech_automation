import pandas as pd

def financial_copilot(question, df, kpis, monthly_data, risk):

    q = question.lower()

    # solde
    if "solde" in q or "balance" in q:
        return f"Le solde net actuel est de {kpis['net_balance']:,.0f} XAF."

    # transactions
    if "transactions" in q:
        return f"Le système contient {kpis['total_transactions']} transactions."

    # revenus
    if "revenu" in q:
        return f"Les revenus totaux sont {kpis['total_income']:,.0f} XAF."

    # dépenses
    if "dépense" in q:
        return f"Les dépenses totales sont {kpis['total_expenses']:,.0f} XAF."

    # compte le plus actif
    if "compte" in q:
        top = df.groupby("account_number")["amount"].sum().idxmax()
        return f"Le compte le plus actif est {top}."

    # tendance
    if "tendance" in q or "évolution" in q:

        if len(monthly_data) > 1:

            if monthly_data[-1] > monthly_data[-2]:
                return "La tendance financière est à la hausse."
            else:
                return "La tendance financière est à la baisse."

        return "Pas assez de données pour analyser la tendance."

    # fraude
    if "fraude" in q or "risque" in q:

        score = risk.get("risk_score", 50)

        if score > 70:
            return f"Risque élevé détecté ({score}/100). Une investigation est recommandée."

        if score > 40:
            return f"Risque modéré ({score}/100). Une surveillance est recommandée."

        return f"Risque faible ({score}/100). Activité normale."

    return "Je peux analyser votre activité financière : solde, revenus, dépenses, comptes ou fraude."


