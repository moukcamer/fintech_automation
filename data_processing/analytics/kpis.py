from django.db.models import Sum
from finance.models import Payment

def global_kpis():
    income = Payment.objects.filter(payment_type="IN").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    expense = Payment.objects.filter(payment_type="OUT").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    return {
        "income": income,
        "expense": expense,
        "net": income - expense
    }
