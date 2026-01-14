from django.db.models import Sum
from finance.models import Payment


def payments_by_month():
    qs = (
        Payment.objects
        .values("created_at__month")
        .annotate(total=Sum("amount"))
        .order_by("created_at__month")
    )

    labels = [f"M{p['created_at__month']}" for p in qs]
    data = [float(p["total"]) for p in qs]

    return labels, data
