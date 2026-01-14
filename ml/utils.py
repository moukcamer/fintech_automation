import pandas as pd
from finance.models import Payment


def get_monthly_payments_df():
    qs = Payment.objects.all().values("date", "amount")
    df = pd.DataFrame(qs)

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df = df.groupby("month")["amount"].sum().reset_index()

    return df
