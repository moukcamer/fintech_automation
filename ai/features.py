# ai/features.py
import pandas as pd

def build_features(df):
    if df.empty:
        return df

    df["amount"] = df["amount"].astype(float)

    # débit / crédit
    df["is_debit"] = (df["transaction_type"] == "OUT").astype(int)
    df["is_credit"] = (df["transaction_type"] == "IN").astype(int)

    # taille transaction
    df["large_transaction"] = df["amount"] > df["amount"].quantile(0.90)

    # activité compte
    activity = df.groupby("account_id")["amount"].count().rename("tx_count")
    df = df.join(activity, on="account_id")

    return df
