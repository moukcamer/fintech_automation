from finance.models import Payment
from django.db.models import Sum


def cashflow_alert(threshold=100000):
    expense = Payment.objects.filter(payment_type="OUT").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    if expense > threshold:
        return f"Alerte : dépenses élevées ({expense} FCFA)"
    return None
