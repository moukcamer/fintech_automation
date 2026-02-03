import pandas as pd
from prophet import Prophet

def build_cashflow_dataframe(queryset):
    df = pd.DataFrame(list(queryset.values(
        "date",
        "amount",
        "transaction_type"
    )))

    if df.empty:
        return df

    # Cash-flow = IN - OUT
    df["signed_amount"] = df.apply(
        lambda x: x["amount"] if x["transaction_type"] == "IN" else -x["amount"],
        axis=1
    )

    # Agrégation journalière
    df = df.groupby("date", as_index=False)["signed_amount"].sum()

    # Format Prophet
    df = df.rename(columns={
        "date": "ds",
        "signed_amount": "y"
    })

    return df

def forecast_cashflow(df, periods=90):
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
