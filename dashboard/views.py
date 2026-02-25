# dashboard/views.py
from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate, TruncMonth
from accounting.models import Payment
from datetime import datetime
import json
from decimal import Decimal
import pandas as pd
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from ai.features import build_features
from ai.risk_engine import compute_risk
from ai.insights import generate_insight
from django.contrib.auth.decorators import login_required

from django.utils import timezone
from datetime import timedelta

from finance.models import Transaction, Account, Customer
from accounting.models import JournalEntry
from fraud.models import FraudAlert
from ai.models import AITransactionScore


@login_required(login_url="/login/")
@cache_page(60)


# ================= AI ENGINE =================
def compute_ai_analysis(transactions):

    if not transactions.exists():
        return {
            "score": 0,
            "text": "Aucune donnée disponible pour analyse."
        }

    total = transactions.count()
    high_amount = transactions.filter(amount__gt=500000).count()
    foreign = transactions.exclude(country="CM").count()

    risk_score = min(100, int((high_amount/total)*60 + (foreign/total)*40))

    if risk_score > 70:
        insight = "Risque élevé : activité inhabituelle détectée."
    elif risk_score > 40:
        insight = "Activité modérément atypique."
    else:
        insight = "Activité financière normale."

    return {
        "score": risk_score,
        "text": insight
    }




def dashboard(request):

    today = timezone.now()
    last_30_days = today - timedelta(days=30)

    transactions = Transaction.objects.select_related(
        "account__customer"
    )

    # ==========================
    # KPI CORE
    # ==========================

    total_transactions = transactions.count()

    total_volume = transactions.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_customers = Customer.objects.count()
    total_accounts = Account.objects.count()

    # ==========================
    # FRAUD & AI
    # ==========================

    fraud_count = FraudAlert.objects.count()

    high_risk_transactions = AITransactionScore.objects.filter(
        risk_score__gte=75
    ).count()

    avg_risk_score = AITransactionScore.objects.aggregate(
        avg=Avg("risk_score")
    )["avg"] or 0

    fraud_rate = (
        (fraud_count / total_transactions) * 100
        if total_transactions > 0 else 0
    )

    # ==========================
    # CASHFLOW
    # ==========================

    inflow = transactions.filter(
        transaction_type="credit"
    ).aggregate(total=Sum("amount"))["total"] or 0

    outflow = transactions.filter(
        transaction_type="debit"
    ).aggregate(total=Sum("amount"))["total"] or 0

    net_cashflow = inflow - outflow

    # ==========================
    # 30 DAYS TREND
    # ==========================

    monthly_trend = (
        transactions
        .filter(created_at__gte=last_30_days)
        .values("created_at__date")
        .annotate(total=Sum("amount"))
        .order_by("created_at__date")
    )

    # ==========================
    # BY TYPE
    # ==========================

    transactions_by_type = (
        transactions
        .values("transaction_type")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )

    # ==========================
    # TOP ACCOUNTS
    # ==========================

    top_accounts = (
        Account.objects
        .annotate(total_volume=Sum("transactions__amount"))
        .order_by("-total_volume")[:10]
    )

    context = {
        "total_transactions": total_transactions,
        "total_volume": total_volume,
        "total_customers": total_customers,
        "total_accounts": total_accounts,
        "fraud_count": fraud_count,
        "high_risk_transactions": high_risk_transactions,
        "avg_risk_score": round(avg_risk_score, 2),
        "fraud_rate": round(fraud_rate, 2),
        "inflow": inflow,
        "outflow": outflow,
        "net_cashflow": net_cashflow,
        "monthly_trend": list(monthly_trend),
        "transactions_by_type": list(transactions_by_type),
        "top_accounts": top_accounts,
    }

    return render(request, "dashboard/dashboard.html", context)




# ================= API CHARTS =================

def monthly_transactions(request):
    qs = (
        Transaction.objects
        .annotate(month=TruncMonth("transaction_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )
    labels = [m["month"].strftime("%b %Y") if m["month"] else "" for m in qs]
    data = [float(m["total"]) for m in qs]
    return JsonResponse({"labels": labels, "data": data})


def transaction_types(request):
    qs = Transaction.objects.values("transaction_type").annotate(total=Count("id"))
    labels = [x["transaction_type"] for x in qs]
    data = [x["total"] for x in qs]
    return JsonResponse({"labels": labels, "data": data})


def top_accounts(request):
    qs = (
        Transaction.objects
        .values("account__account_number")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:5]
    )
    labels = [x["account__account_number"] for x in qs]
    data = [float(x["total"]) for x in qs]
    return JsonResponse({"labels": labels, "data": data})