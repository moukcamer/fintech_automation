def detect_trend(monthly_df):
    cashflow = monthly_df["cashflow"]

    if cashflow.tail(3).mean() > cashflow.head(3).mean():
        return "Croissance"
    elif cashflow.tail(3).mean() < cashflow.head(3).mean():
        return "Ralentissement"
    else:
        return "Stable"
