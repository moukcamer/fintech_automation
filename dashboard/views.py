from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.db.models import Sum
import json
from dashboard.models import Account, Transaction,Payment,Invoice, Customer



def dashboard(request):
    """
    Vue principale du tableau de bord fintech_automation
    - KPIs
    - Filtres
    - Graphiques Chart.js
    - Listes récentes
    """

    # -----------------------------
    # 1. Récupération des filtres
    # -----------------------------
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")
    t_type = request.GET.get("t_type")

    start_date = parse_date(start) if start else None
    end_date = parse_date(end) if end else None

    # -----------------------------
    # 2. KPI GLOBAUX
    # -----------------------------
    total_balance = Account.objects.aggregate(Sum("balance"))["balance__sum"] or 0

    total_income = Payment.objects.filter(payment_type="IN").aggregate(Sum("amount"))["amount__sum"] or 0
    total_expenses = Payment.objects.filter(payment_type="OUT").aggregate(Sum("amount"))["amount__sum"] or 0

    pending_invoices = Invoice.objects.filter(status="PENDING").count()

    # -----------------------------
    # 3. Evolution mensuelle (payments)
    # -----------------------------
    payments = (
        Payment.objects.values("date__month")
        .annotate(total=Sum("amount"))
        .order_by("date__month")
    )

    chart_labels = [f"M{p['date__month']}" for p in payments]
    chart_data = [float(p["total"]) for p in payments]

    # -----------------------------
    # 4. Répartition des comptes
    # -----------------------------
    accounts = Account.objects.select_related("customer").all()

    acc_labels = [
        f"{acc.customer.user.username} ({acc.get_account_type_display()})"
        for acc in accounts
    ]
    acc_data = [float(acc.balance) for acc in accounts]

    # -----------------------------
    # 5. Transactions filtrées
    # -----------------------------
    tqs = Transaction.objects.all()

    if start_date:
        tqs = tqs.filter(issued_at__gte=start_date)

    if end_date:
        tqs = tqs.filter(issued_at__lte=end_date)

    if t_type:
        tqs = tqs.filter(transaction_type=t_type)

    # tri selon ton modèle : created_at existe maintenant ✔
    recent_transactions = tqs.order_by("-created_at")[:10]

    # -----------------------------
    # 6. Factures récentes
    # -----------------------------
    recent_invoices = Invoice.objects.order_by("-issued_at")[:10]

    # -----------------------------
    # 7. Contexte envoyé au template
    # -----------------------------
    
    context = {
        # KPI
        "total_balance": abs(total_balance),
        "total_income": abs(total_income),
        "total_expenses": abs(total_expenses),
        "pending_invoices": pending_invoices,

        # Charts
        "chart_labels_json": json.dumps(chart_labels),
        "chart_data_json": json.dumps(chart_data),
        "acc_labels_json": json.dumps(acc_labels),
        "acc_data_json": json.dumps(acc_data),

        # Tables récentes
        "chart_json": json.dumps(chart_data),
        "recent_transactions": recent_transactions,
        "recent_invoices": recent_invoices,
    }

    return render(request, "dashboard/dashboard.html", context)




