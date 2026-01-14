import pandas as pd
from finance.models import Customer, Payment
from django.db.models import Sum


def customer_score(customer: Customer):
    """
    Scoring simple basé sur l’historique de paiement
    """
    payments = Payment.objects.filter(customer=customer)

    total_in = payments.filter(payment_type="IN").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    total_out = payments.filter(payment_type="OUT").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    balance = total_in - total_out

    if balance > 1_000_000:
        return "A"
    elif balance > 300_000:
        return "B"
    return "C"
