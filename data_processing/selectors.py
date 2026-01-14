from finance.models import Payment, Invoice


def recent_payments(limit=10):
    return Payment.objects.order_by("-created_at")[:limit]


def recent_invoices(limit=10):
    return Invoice.objects.order_by("-created_at")[:limit]
