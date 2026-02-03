def add_time_features(df):
    df["day"] = df["date"].dt.day
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    df["weekday"] = df["date"].dt.weekday
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)

    # Rolling metrics
    df = df.sort_values("date")
    df["rolling_7"] = df["amount_clean"].rolling(7).mean()
    df["rolling_30"] = df["amount_clean"].rolling(30).mean()

    return df
