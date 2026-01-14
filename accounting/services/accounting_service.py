from django.utils import timezone
from accounting.models import Entry, EntryLine, Account, Journal
from decimal import Decimal
from django.db import transaction
from finance.models import Payment


class AccountingService:
    """
    Service central de génération comptable
    """

    @staticmethod
    def get_or_create_journal(code, name, journal_type):
        journal, _ = Journal.objects.get_or_create(
            code=code,
            defaults={
                "name": name,
                "journal_type": journal_type
            }
        )
        return journal

    @staticmethod
    def post_entry(
        reference,
        description,
        debit_account_code,
        credit_account_code,
        amount,
        journal_code="BNK"
    ):
        journal = AccountingService.get_or_create_journal(
            journal_code, "Banque", "BANK"
        )

        debit_account = Account.objects.get(code=debit_account_code)
        credit_account = Account.objects.get(code=credit_account_code)

        entry = Entry.objects.create(
            journal=journal,
            date=timezone.now().date(),
            reference=reference,
            description=description,
        )

        EntryLine.objects.create(
            entry=entry,
            account=debit_account,
            debit=amount
        )

        EntryLine.objects.create(
            entry=entry,
            account=credit_account,
            credit=amount
        )

        # Mise à jour des soldes
        debit_account.balance += amount
        credit_account.balance -= amount

        debit_account.save()
        credit_account.save()

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
