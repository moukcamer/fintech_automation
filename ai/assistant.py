import pandas as pd

def financial_copilot(question, df, kpis):

    q = question.lower()

    if "solde" in q or "balance" in q:
        return f"Le solde net actuel est de {kpis['net_balance']:,.0f} XAF."

    elif "transactions" in q:
        return f"Le système contient {kpis['total_transactions']} transactions."

    elif "revenu" in q or "income" in q:
        return f"Les revenus totaux sont de {kpis['total_income']:,.0f} XAF."

    elif "dépense" in q or "expense" in q:
        return f"Les dépenses totales sont de {kpis['total_expenses']:,.0f} XAF."

    elif "compte" in q:
        top = df.groupby("account_number")["amount"].sum().idxmax()
        return f"Le compte le plus actif est {top}."

    else:
        return "Je peux analyser vos finances. Essayez par exemple : solde, revenus, dépenses ou comptes."