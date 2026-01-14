from django.db.models import Sum
from finance.models import Payment, Invoice, Account


def compute_financial_kpis():
    return {
        "total_balance": Account.objects.aggregate(
            total=Sum("balance")
        )["total"] or 0,

        "total_income": Payment.objects.filter(
            payment_type="IN"
        ).aggregate(total=Sum("amount"))["total"] or 0,

        "total_expenses": Payment.objects.filter(
            payment_type="OUT"
        ).aggregate(total=Sum("amount"))["total"] or 0,

        "pending_invoices": Invoice.objects.filter(
            status="UNPAID"
        ).count(),
    }
