from finance.models import Payment
from django.db.models import Sum
from django.utils.timezone import now


def compute_daily_kpis():
    today = now().date()

    income = Payment.objects.filter(
        created_at__date=today,
        payment_type="IN"
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    expense = Payment.objects.filter(
        created_at__date=today,
        payment_type="OUT"
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    return {
        "date": today,
        "income": income,
        "expense": expense,
        "net": income - expense
    }
