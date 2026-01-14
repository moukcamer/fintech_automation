from django.db.models.signals import post_save
from django.dispatch import receiver
from finance.models import Payment
from accounting.models import Account
from accounting.services import record_double_entry


@receiver(post_save, sender=Payment)
def payment_to_accounting(sender, instance, created, **kwargs):
    if not created:
        return

    # Compte de caisse / banque
    cash_account = Account.objects.get(code="101")
    

    # =======================
    # PAIEMENT ENTRANT
    # =======================
    if instance.payment_type == "IN":
        income_account = Account.objects.get(code="701")

        record_double_entry(
            date=instance.date,
            description=f"Encaissement paiement #{instance.id}",
            debit_account=cash_account,
            credit_account=income_account,
            amount=instance.amount,
            reference=f"PAY-IN-{instance.id}"
        )

    # =======================
    # PAIEMENT SORTANT
    # =======================
    else:
        expense_account = Account.objects.get(code="601")

        record_double_entry(
            date=instance.date,
            description=f"Décaissement paiement #{instance.id}",
            debit_account=expense_account,
            credit_account=cash_account,
            amount=instance.amount,
            reference=f"PAY-OUT-{instance.id}"
        )
