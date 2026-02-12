# dashboard/views.py
from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from finance.models import Transaction, Account
from datetime import datetime
import json
from decimal import Decimal
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from ai.features import build_features
from ai.risk_engine import compute_risk
from ai.insights import generate_insight
from django.contrib.auth.decorators import login_required

@login_required
@cache_page(60)  # 60 secondes
@login_required(login_url="/login/")



def dashboard(request):
    # =============================
    # Filtres (Slicers)
    # =============================
    queryset = Transaction.objects.all()
    date_start = request.GET.get('date_start')
    date_end = request.GET.get('date_end')
    transaction_type = request.GET.get('transaction_type')
    account_id = request.GET.get('account')

    if date_start:
        queryset = queryset.filter(date__gte=datetime.strptime(date_start, '%d/%m/%Y'))
    if date_end:
        queryset = queryset.filter(date__lte=datetime.strptime(date_end, '%d/%m/%Y'))
    if transaction_type:
        queryset = queryset.filter(transaction_type=transaction_type)
    if account_id:
        queryset = queryset.filter(account_id=account_id)
    

    # =============================
    # KPIs (sur queryset filtré)
    # =============================
    total_transactions = queryset.count()
    total_amount = float(queryset.aggregate(total=Sum('amount'))['total'] or Decimal('0'))
    total_income = float(queryset.filter(transaction_type='IN').aggregate(total=Sum('amount'))['total'] or Decimal('0'))
    total_expenses = float(queryset.filter(transaction_type='OUT').aggregate(total=Sum('amount'))['total'] or Decimal('0'))
    net_balance = total_income - total_expenses
    total_customers = (queryset.filter(account__customer__isnull=False).values('account__customer').distinct().count())
    total_accounts = Account.objects.count()  # Global, pas filtré

    # =============================
    # Chart Évolution
    # =============================
    daily_data = queryset.annotate(day=TruncDate('transaction_date')).values('day').annotate(total=Sum('amount')).order_by('day')
    chart_dates = [entry['day'].strftime('%d/%m/%Y') for entry in daily_data]
    chart_amounts = [float(entry['total'] or 0) for entry in daily_data]

    # =============================
    # Chart Types
    # =============================
    type_data = queryset.values('transaction_type').annotate(total=Sum('amount')).order_by('-total')
    type_labels = [entry['transaction_type'] or 'Inconnu' for entry in type_data]
    type_amounts = [float(entry['total'] or 0) for entry in type_data]

    # =============================
    # Nouveau Chart Comptes (Barres)
    # =============================
    account_data = queryset.values('account__account_number').annotate(total=Sum('amount')).order_by('-total')
    account_labels = [entry['account__account_number'] or 'Compte Inconnu' for entry in account_data]
    account_amounts = [float(entry['total'] or 0) for entry in account_data]

    # =============================
    # Dernières Transactions
    # =============================
    latest_transactions = queryset.select_related('account', 'account__customer').order_by('-transaction_date')[:20]



   # =============================
   # IA ANALYSIS
   # =============================


# Préparation des données pour l'IA
    qs = queryset.values(
        "amount",
        "transaction_type",
        "account__account_number"   # ← correction : account__account_number (pas account_id seul)
        ).order_by("transaction_date")

    df = pd.DataFrame(list(qs))

    ai_result = {
        "score": 50,               # valeur par défaut en cas d'échec
        "alerts": [],
        "text": "Aucune donnée suffisante pour analyse"
        }

    if not df.empty:
        try:
        # Ajout des features (supposé que cette fonction existe)
            df = build_features(df)

        # Calcul du risque (supposé que cette fonction existe)
            risk = compute_risk(df)

        # Génération du texte d'insight
            ai_text = generate_insight(
                context={
                    "net_balance": net_balance,
                    "total_transactions": total_transactions,
                    "total_amount": df['amount'].sum() if 'amount' in df else 0,
                },
                risk=risk
            )

            ai_result = {
                "score": risk.get("risk_score", 50),
                "alerts": risk.get("alerts", []),
                "text": ai_text or "Analyse terminée sans recommandation particulière.",
                "model_used": "Analyse basique 2025",  # optionnel
            }

        except Exception as e:
        # En cas d'erreur dans les fonctions IA
            ai_result["text"] = f"Erreur lors de l'analyse IA : {str(e)}"
            ai_result["alerts"] = ["Analyse impossible - données insuffisantes ou erreur technique"]




    # =============================
    # Contexte
    # =============================
    context = {
        'kpi': {
            'total_transactions': total_transactions,
            'total_amount': round(total_amount, 2),
            'net_balance': round(net_balance, 2),
            'total_customers': total_customers,
            'total_accounts': total_accounts,
        },
        'chart_evolution': {
            'labels': json.dumps(chart_dates),
            'data': json.dumps(chart_amounts),
        },
        'chart_types': {
            'labels': json.dumps(type_labels),
            'data': json.dumps(type_amounts),
        },
        'chart_accounts': {  # Nouveau
            'labels': json.dumps(account_labels),
            'data': json.dumps(account_amounts),
        },
        'latest_transactions': latest_transactions,
        'accounts': Account.objects.all(),  # Pour select filtre

        'ai':ai_result,
    }


    return render(request, 'dashboard/dashboard.html', context)