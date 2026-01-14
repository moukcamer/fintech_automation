from django.shortcuts import render
from django.db.models import Sum
from django.utils.dateparse import parse_date
import json

from finance.models import Payment, Invoice, Account


def dashboard(request):
    """
    Vue principale du dashboard PowerBI-like
    """

    # ===============================
    # 1. FILTRES (dates)
    # ===============================
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")

    start_date = parse_date(start) if start else None
    end_date = parse_date(end) if end else None

    # ===============================
    # 2. KPIs
    # ===============================
    total_balance = (
        Account.objects.aggregate(total=Sum("balance"))["total"] or 0
    )

    total_income = (
        Payment.objects
        .filter(payment_type="IN")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_expenses = (
        Payment.objects
        .filter(payment_type="OUT")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    pending_invoices = (
        Invoice.objects
        .filter(status="PENDING")
        .count()
    )

    # ===============================
    # 3. ÉVOLUTION MENSUELLE (Payments)
    # ===============================
    payments_qs = Payment.objects.exclude(date__isnull=True)

    if start_date:
        payments_qs = payments_qs.filter(date__gte=start_date)
    if end_date:
        payments_qs = payments_qs.filter(date__lte=end_date)

    monthly_payments = (
        payments_qs
        .values("date__month")
        .annotate(total=Sum("amount"))
        .order_by("date__month")
    )

    chart_labels = [f"M{p['date__month']}" for p in monthly_payments]
    chart_data = [float(p["total"]) for p in monthly_payments]

    # ===============================
    # 4. RÉPARTITION DES COMPTES
    # ===============================
    accounts = Account.objects.all()

    acc_labels = [acc.name for acc in accounts]
    acc_data = [float(acc.balance) for acc in accounts]

    # ===============================
    # 5. TRANSACTIONS RÉCENTES
    # ===============================
    recent_transactions = (
        Payment.objects
        .select_related("account")
        .exclude(date__isnull=True)
        .order_by("-date")[:10]
    )

    # ===============================
    # 6. FACTURES RÉCENTES
    # ===============================
    recent_invoices = (
        Invoice.objects
        .exclude(created_at__isnull=True)
        .order_by("-created_at")[:10]
    )

    # ===============================
    # 7. CONTEXTE TEMPLATE
    # ===============================
    context = {
        # KPIs
        "total_balance": total_balance,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "pending_invoices": pending_invoices,

        # Charts
        "chart_labels_json": json.dumps(chart_labels),
        "chart_data_json": json.dumps(chart_data),
        "acc_labels_json": json.dumps(acc_labels),
        "acc_data_json": json.dumps(acc_data),

        # Tables
        "recent_transactions": recent_transactions,
        "recent_invoices": recent_invoices,
    }

    return render(request, "dashboard/dashboard.html", context)
