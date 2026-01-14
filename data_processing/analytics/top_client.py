from finance.models import Invoice
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse


def top_clients(request):
    qs = (
        Invoice.objects
        .values("customer_name")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:5]
    )

    return JsonResponse({
        "labels": [c["customer_name"] for c in qs],
        "values": [float(c["total"]) for c in qs]
    })

