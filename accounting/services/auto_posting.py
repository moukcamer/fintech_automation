from decimal import Decimal
from django.utils import timezone
from accounting.models import JournalEntry, JournalLine, Account as GLAccount


def get_gl_accounts(transaction):
    """
    Mapping transaction → plan comptable OHADA simplifié
    """

    # Comptes par défaut
    bank = GLAccount.objects.get(code="512000")
    sales = GLAccount.objects.get(code="701000")
    expense = GLAccount.objects.get(code="601000")

    if transaction.transaction_type == "IN":
        return bank, sales, "CREDIT"
    else:
        return expense, bank, "DEBIT"


def post_transaction_to_ledger(transaction):

    if transaction.is_posted:
        return

    debit_acc, credit_acc, direction = get_gl_accounts(transaction)

    # Création écriture
    entry = JournalEntry.objects.create(
        date=timezone.now(),
        reference=transaction.transaction_ref,
        description=transaction.description or "Auto posting",
        source="SYSTEM"
    )

    amount = Decimal(transaction.amount)

    if direction == "CREDIT":
        JournalLine.objects.create(
            entry=entry,
            account=debit_acc,
            debit=amount,
            credit=Decimal("0.00")
        )

        JournalLine.objects.create(
            entry=entry,
            account=credit_acc,
            debit=Decimal("0.00"),
            credit=amount
        )

    else:
        JournalLine.objects.create(
            entry=entry,
            account=credit_acc,
            debit=amount,
            credit=Decimal("0.00")
        )

        JournalLine.objects.create(
            entry=entry,
            account=debit_acc,
            debit=Decimal("0.00"),
            credit=amount
        )

    # Marquer comme comptabilisée
    transaction.is_posted = True
    transaction.posted_at = timezone.now()
    transaction.status = "POSTED"
    transaction.save(update_fields=["is_posted", "posted_at", "status"])

