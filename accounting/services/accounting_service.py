from django.utils import timezone
from decimal import Decimal
from django.db import transaction
from finance.models import Payment
from django.core.exceptions import ValidationError
from finance.models import Account
from accounting.models import JournalEntry, JournalLine, Entry, Journal


class AccountingService:

    @staticmethod
    @transaction.atomic
    def post_entry(
        debit_account_number: str,
        credit_account_number: str,
        amount: float,
        description: str = "",
        reference: str = None
    ):
        """
        Crée une écriture comptable équilibrée.
        """

        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        # 🔎 Récupération des comptes
        try:
            debit_account = Account.objects.get(
                account_number=debit_account_number
            )
        except Account.DoesNotExist:
            raise ValidationError(
                f"Debit account {debit_account_number} not found."
            )

        try:
            credit_account = Account.objects.get(
                account_number=credit_account_number
            )
        except Account.DoesNotExist:
            raise ValidationError(
                f"Credit account {credit_account_number} not found."
            )

        # 🧾 Création Journal Entry
        entry = JournalEntry.objects.create(
            reference=reference,
            description=description,
            is_posted=False
        )

        # ➕ Ligne Débit
        JournalLine.objects.create(
            journal_entry=entry,
            account=debit_account,
            debit=amount,
            credit=0
        )

        # ➖ Ligne Crédit
        JournalLine.objects.create(
            journal_entry=entry,
            account=credit_account,
            debit=0,
            credit=amount
        )

        # ✅ Marquer comme posté
        entry.is_posted = True
        entry.save()

        return entry




# ===============================
# ENREGISTRER UN PAIEMENT
# ===============================
@transaction.atomic
def record_payment(
    *,
    amount: Decimal,
    payment_type: str,
    debit_account: Account,
    credit_account: Account,
    reference: str = ""
):
    """
    Enregistre un paiement et met à jour les comptes
    payment_type : IN | OUT
    """

    if amount <= 0:
        raise ValueError("Le montant doit être supérieur à zéro")

    # 1. Créer le paiement
    payment = Payment.objects.create(
        amount=amount,
        payment_type=payment_type,
        reference=reference
    )

    # 2. Mouvement comptable
    if payment_type == "IN":
        debit_account.balance += amount
        credit_account.balance -= amount
    elif payment_type == "OUT":
        debit_account.balance -= amount
        credit_account.balance += amount
    else:
        raise ValueError("Type de paiement invalide")

    debit_account.save()
    credit_account.save()

    return payment
