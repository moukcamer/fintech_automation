from finance.models import Payment
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse

def monthly_performance(request):
    qs = (
        Payment.objects
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    labels = [p["month"].strftime("%b %Y") for p in qs]
    values = [float(p["total"]) for p in qs]

    return JsonResponse({
        "labels": labels,
        "values": values
    })
