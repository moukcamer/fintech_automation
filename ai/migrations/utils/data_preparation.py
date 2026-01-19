import pandas as pd

def prepare_financial_data(queryset):
    df = pd.DataFrame(list(queryset.values()))
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df["income"] = df.apply(
        lambda x: x["amount"] if x["transaction_type"] == "income" else 0,
        axis=1
    )
    df["expense"] = df.apply(
        lambda x: x["amount"] if x["transaction_type"] == "expense" else 0,
        axis=1
    )

    monthly = df.resample("M", on="date").sum()
    monthly["cashflow"] = monthly["income"] - monthly["expense"]

    return monthly
