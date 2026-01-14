from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from finance.models import Payment


def monthly_performance(request):
    data = (
        Payment.objects
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    return JsonResponse({
        "labels": [d["month"].strftime("%Y-%m") for d in data],
        "values": [float(d["total"]) for d in data],
    })
