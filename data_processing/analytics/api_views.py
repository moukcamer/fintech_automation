from django.http import JsonResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from finance.models import Payment


def monthly_performance(request):
    """
    Performance financière mensuelle
    API REST → Dashboard PowerBI-like
    """
    qs = (
        Payment.objects
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    return JsonResponse({
        "labels": [
            item["month"].strftime("%Y-%m")
            for item in qs if item["month"]
        ],
        "values": [
            float(item["total"])
            for item in qs
        ]
    })
