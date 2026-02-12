import pandas as pd
from sklearn.linear_model import LinearRegression
from finance.models import Transaction
from django.db.models.functions import TruncMonth
from django.db.models import Sum


def forecast_cashflow():

    qs = (
        Transaction.objects
        .annotate(month=TruncMonth("transaction_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    df = pd.DataFrame(list(qs))

    if len(df) < 3:
        return None

    df["t"] = range(len(df))

    model = LinearRegression()
    model.fit(df[["t"]], df["total"])

    next_month = model.predict([[len(df)]])[0]

    return round(next_month, 2)