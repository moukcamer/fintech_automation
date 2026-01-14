from decimal import Decimal
from django.db import transaction
from accounting.models import Account


@transaction.atomic
def handle_payment(payment):
    """
    Gère l'impact comptable d'un paiement
    """
    amount = Decimal(payment.amount)

    if payment.payment_type == "IN":
        account = Account.objects.first()
        account.balance += amount
    else:
        account = Account.objects.first()
        account.balance -= amount

    account.save()
