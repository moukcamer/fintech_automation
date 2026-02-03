#accounting/sevices.py

from accounting.models import Account, Journal, Entry, EntryLine, JournalEntry,Transaction, Invoice, Payment, AccountingPeriod
from decimal import Decimal
from django.db import transaction
from django.utils import timezone


def record_payment(payment):
    cash = Account.objects.get(code="101")  # Caisse
    journal = Journal.objects.get(code="BNK")

    if payment.payment_type == "IN":
        income = Account.objects.get(code="701")  # Revenus

        entry = Entry.objects.create(
            journal=journal,
            reference=f"PAY-{payment.id}",
            description=payment.description
        )

        EntryLine.objects.create(entry=entry, account=cash, debit=payment.amount)
        EntryLine.objects.create(entry=entry, account=income, credit=payment.amount)

    else:
        expense = Account.objects.get(code="601")  # Charges

        entry = Entry.objects.create(
            journal=journal,
            reference=f"PAY-{payment.id}",
            description=payment.description
        )

        EntryLine.objects.create(entry=entry, account=expense, debit=payment.amount)
        EntryLine.objects.create(entry=entry, account=cash, credit=payment.amount)

from django.db.models import Sum


def profit_and_loss():
    income = Account.objects.filter(account_type="INCOME").aggregate(
        total=Sum("balance")
    )["total"] or 0

    expenses = Account.objects.filter(account_type="EXPENSE").aggregate(
        total=Sum("balance")
    )["total"] or 0

    return {
        "income": income,
        "expenses": expenses,
        "net_result": income - expenses
    }

def balance_sheet():
    assets = Account.objects.filter(account_type="ASSET")
    liabilities = Account.objects.filter(account_type="LIABILITY")
    equity = Account.objects.filter(account_type="EQUITY")

    return {
        "assets": assets,
        "liabilities": liabilities,
        "equity": equity,
    }

def cash_flow():
    cash = Account.objects.get(code="101")
    return {
        "cash_balance": cash.balance
    }


@transaction.atomic
def record_double_entry(
    *,
    date,
    description,
    debit_account,
    credit_account,
    amount,
    reference=None
):
    # Sécurité
    if not hasattr(debit_account, "id"):
        raise TypeError("debit_account doit être une instance Account")

    if not hasattr(credit_account, "id"):
        raise TypeError("credit_account doit être une instance Account")

    if amount <= 0:
        raise ValueError("Le montant doit être positif")

    JournalEntry.objects.create(
        date=date,
        description=description,
        account=debit_account,   # ✅ instance Account
        debit=Decimal(amount),
        credit=Decimal("0.00"),
        reference=reference,
    )

    JournalEntry.objects.create(
        date=date,
        description=description,
        account=credit_account,  # ✅ instance Account
        debit=Decimal("0.00"),
        credit=Decimal(amount),
        reference=reference,
    )





def close_period(month, year):
    period, _ = AccountingPeriod.objects.get_or_create(
        month=month,
        year=year
    )

    if period.is_closed:
        raise Exception("Cette période est déjà clôturée")

    period.is_closed = True
    period.closed_at = timezone.now()
    period.save()

    return period

from accounting.models import AccountingPeriod


def is_period_closed(date):
    return AccountingPeriod.objects.filter(
        month=date.month,
        year=date.year,
        is_closed=True
    ).exists()
