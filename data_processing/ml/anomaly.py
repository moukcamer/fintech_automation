def detect_anomalies(df, threshold=2):
    mean = df["amount"].mean()
    std = df["amount"].std()
    return df[df["amount"] > mean + threshold * std]
