from django.shortcuts import render
from django.db.models import Sum, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from datetime import datetime
import pandas as pd
import json

# IA modules
from ai.features import build_features
from ai.risk_engine import compute_risk
from ai.insights import generate_insight
from ai.narration import generate_narrative

from finance.models import Account, Transaction


@login_required(login_url="/login/")
@cache_page(60 * 5)
def dashboard(request):

    # =====================================================
    # 1️⃣ QUERYSET DE BASE + FILTRES
    # =====================================================
    queryset = Transaction.objects.select_related("account").all()

    date_start = request.GET.get("date_start", "").strip()
    date_end = request.GET.get("date_end", "").strip()
    trans_type = request.GET.get("transaction_type", "").strip()
    account_id = request.GET.get("account", "").strip()

    if date_start:
        try:
            dt_start = datetime.strptime(date_start, "%Y-%m-%d")
            queryset = queryset.filter(transaction_date__date__gte=dt_start)
        except:
            pass

    if date_end:
        try:
            dt_end = datetime.strptime(date_end, "%Y-%m-%d")
            queryset = queryset.filter(transaction_date__date__lte=dt_end)
        except:
            pass

    if trans_type in ["IN", "OUT"]:
        queryset = queryset.filter(transaction_type=trans_type)

    if account_id.isdigit():
        queryset = queryset.filter(account_id=int(account_id))

    # =====================================================
    # 2️⃣ KPIs
    # =====================================================
    total_transactions = queryset.count()

    total_amount = float(
        queryset.aggregate(total=Sum("amount"))["total"] or 0
    )

    total_income = float(
        queryset.filter(amount__gt=0)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_expenses = float(
        queryset.filter(amount__lt=0)
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    net_balance = total_income + total_expenses
    total_accounts = Account.objects.count()

    # =====================================================
    # 3️⃣ GRAPHIQUE ÉVOLUTION QUOTIDIENNE
    # =====================================================
    daily_qs = (
        queryset.annotate(day=TruncDate("transaction_date"))
        .values("day")
        .annotate(
            total_credit=Sum("amount", filter=Q(amount__gt=0)),
            total_debit=Sum("amount", filter=Q(amount__lt=0)),
        )
        .order_by("day")
    )

    evolution_labels = []
    evolution_data = []

    for row in daily_qs:
        if row["day"]:
            evolution_labels.append(row["day"].strftime("%d/%m/%Y"))
            net_day = (row["total_credit"] or 0) + (row["total_debit"] or 0)
            evolution_data.append(float(net_day))

    # =====================================================
    # 4️⃣ GRAPHIQUE MENSUEL
    # =====================================================
    monthly_qs = (
        queryset.annotate(month=TruncMonth("transaction_date"))
        .values("month")
        .annotate(
            total_credit=Sum("amount", filter=Q(amount__gt=0)),
            total_debit=Sum("amount", filter=Q(amount__lt=0)),
        )
        .order_by("month")
    )

    monthly_labels = []
    monthly_data = []

    for row in monthly_qs:
        if row["month"]:
            monthly_labels.append(row["month"].strftime("%b %Y"))
            net_month = (row["total_credit"] or 0) + (row["total_debit"] or 0)
            monthly_data.append(float(net_month))

    # =====================================================
    # 5️⃣ RÉPARTITION PAR TYPE
    # =====================================================
    type_qs = (
        queryset.values("transaction_type")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    type_labels = [row["transaction_type"] for row in type_qs]
    type_data = [float(row["total"] or 0) for row in type_qs]

    # =====================================================
    # 6️⃣ ANALYSE IA + NARRATION
    # =====================================================
    ai_result = {
        "score": 50,
        "alerts": [],
        "text": "Aucune donnée suffisante",
        "model_used": None,
    }

    narrative_text = "Narration indisponible."

    if queryset.exists():
        try:
            df = pd.DataFrame(
                list(
                    queryset.values(
                        "amount",
                        "transaction_type",
                        "account_id",
                        "account__account_number",
                        "transaction_date",
                    ).order_by("transaction_date")
                )
            )

            # Normalisation pour moteur IA
            df.rename(
                columns={
                    "transaction_date": "date",
                    "account__account_number": "account_number",
                },
                inplace=True,
            )

            # Feature engineering
            df = build_features(df)

            # Risk engine
            risk = compute_risk(df)

            if not isinstance(risk, dict):
                risk = {"risk_score": 50, "alerts": []}

            if not isinstance(risk.get("alerts"), list):
                risk["alerts"] = []

            # KPIs pour IA
            kpis = {
                "net_balance": net_balance,
                "total_transactions": total_transactions,
                "total_amount": total_amount,
            }

            insight_text = generate_insight(kpis=kpis, risk=risk)

            narrative_text = generate_narrative(
                kpis=kpis,
                risk=risk,
                monthly_data=monthly_data,
                evolution_data=evolution_data,
            )

            ai_result.update(
                {
                    "score": risk.get("risk_score", 50),
                    "alerts": risk.get("alerts", []),
                    "text": insight_text or "Activité normale détectée",
                    "model_used": "Analyse 2026 v2",
                }
            )

        except Exception as e:
            ai_result["text"] = f"Erreur analyse IA : {str(e)}"
            narrative_text = "Erreur génération narration."

    # =====================================================
    # 7️⃣ TABLE DERNIÈRES TRANSACTIONS
    # =====================================================
    transactions = (
        queryset.select_related("account")
        .order_by("-transaction_date")[:20]
    )

    # =====================================================
    # 8️⃣ CONTEXT TEMPLATE
    # =====================================================
    context = {
        "total_transactions": total_transactions,
        "total_amount": total_amount,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "total_accounts": total_accounts,
        "ai": ai_result,
        "narrative_text": narrative_text,
        "chart_evolution": {
            "labels": json.dumps(evolution_labels),
            "data": json.dumps(evolution_data),
        },
        "chart_monthly": {
            "labels": json.dumps(monthly_labels),
            "data": json.dumps(monthly_data),
        },
        "chart_types": {
            "labels": json.dumps(type_labels),
            "data": json.dumps(type_data),
        },
        "filters": {
            "date_start": date_start,
            "date_end": date_end,
            "transaction_type": trans_type,
            "account_id": account_id,
        },
        "transactions": transactions,
    }

    return render(request, "dashboard/dashboard.html", context)

