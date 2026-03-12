#ml/views.py

from django.shortcuts import render
from finance.models import Transaction
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from ml.forecast import financial_forecast


def forecast_view(request):

    monthly_qs = (
        Transaction.objects
        .annotate(month=TruncMonth("transaction_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    labels = []
    data = []

    for item in monthly_qs:
        labels.append(item["month"].strftime("%b %Y"))
        data.append(float(item["total"] or 0))

    forecast_values = financial_forecast(data, periods=3)

    context = {
        "labels": labels,
        "data": data,
        "forecast": forecast_values
    }

    return render(request, "ml/forecast.html", context)






