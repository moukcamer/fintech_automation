from sklearn.ensemble import IsolationForest

def detect_anomalies(df):
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    df["anomaly"] = model.fit_predict(df)
    df["anomaly_score"] = model.decision_function(df)

    return df
