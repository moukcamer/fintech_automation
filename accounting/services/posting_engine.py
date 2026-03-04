from django.db import transaction
from finance.models import Account,Transaction
from django.db.models import F


def post_transaction(debit_account_number, credit_account_number, amount, description, reference):

    # ✅ Import local pour éviter circular import
    from accounting.models import JournalEntry, JournalLine
    from finance.models import Account

    debit_account = Account.objects.get(account_number=debit_account_number)
    credit_account = Account.objects.get(account_number=credit_account_number)

    entry = JournalEntry.objects.create(
        reference=reference,
        description=description
    )

    JournalLine.objects.create(
        journal_entry=entry,
        account=debit_account,
        debit=amount,
        credit=0
    )

    JournalLine.objects.create(
        journal_entry=entry,
        account=credit_account,
        debit=0,
        credit=amount
    )

    return entry


  
