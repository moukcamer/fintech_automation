import pandas as pd

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    # Suppression des valeurs manquantes critiques
    df = df.dropna(subset=["date", "amount", "transaction_type"])

    # Conversion types
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Outliers (clip intelligent)
    low, high = df["amount"].quantile([0.05, 0.95])
    df["amount_clean"] = df["amount"].clip(low, high)

    return df
