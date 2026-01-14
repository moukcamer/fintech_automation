from django.db.models.functions import TruncMonth
from django.db.models import Sum
from finance.models import Payment

def monthly_trend():
    return (
        Payment.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )
