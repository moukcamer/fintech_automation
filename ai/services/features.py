import pandas as pd

def build_features(queryset):
    df = pd.DataFrame(list(queryset.values(
        "amount",
        "transaction_type",
        "status"
    )))

    if df.empty:
        return df

    # Encodage simple
    df["transaction_type"] = df["transaction_type"].map({"IN": 1, "OUT": -1})
    df["status"] = df["status"].map({
        "completed": 1,
        "pending": 0,
        "failed": -1
    })

    df = df.fillna(0)
    return df
