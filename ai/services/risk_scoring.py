import numpy as np

def financial_risk_score(monthly_df):
    volatility = np.std(monthly_df["cashflow"])
    avg_cash = np.mean(monthly_df["cashflow"])

    score = 100 - (volatility / max(avg_cash, 1)) * 100
    return max(0, min(round(score), 100))
