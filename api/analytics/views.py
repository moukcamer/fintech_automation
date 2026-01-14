from django.db.models import Sum
from django.http import JsonResponse
from finance.models import Payment
from django.db.models.functions import TruncMonth

def monthly_performance(request):
    org = request.organization

    qs = (
        Payment.objects
        .filter(account__company=org)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    labels = [q["month"].strftime("%b %Y") for q in qs]
    values = [float(q["total"]) for q in qs]

    return JsonResponse({
        "labels": labels,
        "values": values
    })

def top_clients(request):
    org = request.organization

    qs = (
        Payment.objects
        .filter(account__company=org)
        .values("invoice__customer_name")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:10]
    )

    return JsonResponse({
        "clients": [q["invoice__customer_name"] for q in qs],
        "amounts": [float(q["total"]) for q in qs]
    })
