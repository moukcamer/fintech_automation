#dashboard/utils.py

from finance.models import Transaction, Invoice, Payment
from .models import Customer, Transaction, Account
from django.db.models import Sum, count
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
import calendar


def get_monthly_chart_data():
    data = (
        Transaction.objects
        .extra(select={'month': "strftime('%%Y-%%m', date)"})
        .values("month", "type")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )
    return data


def get_top_customers(limit=5):
    """
    Retourne les meilleurs clients classés par montant total des transactions.
    """
    return (
        Customer.objects
        .annotate(total_spent=Sum("transaction__amount"))
        .order_by("-total_spent")[:limit]
    )


# -----------------------------
# KPIs pour le dashboard
# -----------------------------
def get_kpi_summary():
    total_revenue = Transaction.objects.filter(transaction_type="deposit").aggregate(total=Sum("amount"))["total"] or 0
    total_expenses = Transaction.objects.filter(transaction_type="withdrawal").aggregate(total=Sum("amount"))["total"] or 0
    balance = total_revenue - total_expenses

    this_month = datetime.now().month
    monthly_revenue = Transaction.objects.filter(
        transaction_type="deposit",
        issued_at__month=this_month
    ).aggregate(total=Sum("amount"))["total"] or 0

    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "balance": balance,
        "monthly_revenue": monthly_revenue,
    }


def get_financial_summary(start=None, end=None):
    qs = Transaction.objects.all()
    if start:
        qs = qs.filter(issued_at__gte=start)
    if end:
        qs = qs.filter(issued_at__lte=end)

    total_income = qs.filter(transaction_type="deposit").aggregate(Sum("amount"))["amount__sum"] or 0
    total_expenses = qs.filter(transaction_type="withdrawal").aggregate(Sum("amount"))["amount__sum"] or 0
    total_balance = Account.objects.aggregate(total=Sum("balance"))["total"] or 0
    pending_invoices = Invoice.objects.filter(status__in=["UNPAID", "PENDING", "unpaid", "pending"]).count()

    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "total_balance": float(total_balance),
        "pending_invoices": int(pending_invoices),
    }


def get_balance_evolution(months=12):
    today = timezone.now().date()
    labels = []
    values = []
    for i in range(months - 1, -1, -1):
        # first day of target month
        year = (today.replace(day=1) - timedelta(days=30 * i)).year
        month = (today.replace(day=1) - timedelta(days=30 * i)).month
        labels.append(f"{calendar.month_abbr[month]} {year}")

        credits = Transaction.objects.filter(
            transaction_type="deposit",
            issued_at__year=year,
            issued_at__month=month
        ).aggregate(total=Sum("amount"))["total"] or 0

        debits = Transaction.objects.filter(
            transaction_type="withdrawal",
            issued_at__year=year,
            issued_at__month=month
        ).aggregate(total=Sum("amount"))["total"] or 0

        values.append(float(credits) - float(debits))

    return labels, values


def get_accounts_distribution():
    qs = Account.objects.values("account_type").annotate(total=Sum("balance")).order_by("account_type")
    labels = [row["account_type"] or "Unknown" for row in qs]
    values = [float(row["total"] or 0) for row in qs]
    return labels, values


def get_recent_transactions(limit=10):
    return Transaction.objects.order_by("-issued_at")[:limit]


def get_recent_invoices(limit=10):
    return Invoice.objects.order_by("-issued_at")[:limit]


def get_chart_data():
    # Balance evolution
    payments = Payment.objects.values("payment_method").annotate(total=Count("id"))


    labels = [f"M{p['date__month']}" for p in payments]
    balance = [float(p["total"]) for p in payments]

    # Accounts distribution
    accounts = Account.objects.values("account_type").annotate(total=Count("id"))

    accounts_labels = [a["account_type"] for a in accounts]
    accounts_values = [a["total"] for a in accounts]

    return {
        "labels": labels,
        "balance": balance,
        "accounts_labels": accounts_labels,
        "accounts_values": accounts_values,
    }

