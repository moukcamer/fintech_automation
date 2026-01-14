from django.db.models import Sum
from finance.models import Payment


def monthly_cashflow():
    income = Payment.objects.filter(
        payment_type="IN"
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = Payment.objects.filter(
        payment_type="OUT"
    ).aggregate(total=Sum("amount"))["total"] or 0

    return {
        "income": income,
        "expense": expense,
        "net": income - expense
    }
