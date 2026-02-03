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
    total_customers = queryset.exclude(account__customer__isnull=False).values('account__customer').distinct().count()
    total_accounts = Account.objects.count()  # Global, pas filtré
    Transaction.objects.aggregate(total=Sum("amount"))

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
    account_labels = [entry['account__account_number'] or 'Inconnu' for entry in account_data]
    account_amounts = [float(entry['total'] or 0) for entry in account_data]

    # =============================
    # Dernières Transactions
    # =============================
    latest_transactions = queryset.select_related('account', 'account__customer').order_by('-transaction_date')[:20]

        # =============================
    # 6. IA PIPELINE
    # =============================

    qs = Transaction.objects.filter(transaction_type__in=["IN", "OUT"])

    df = pd.DataFrame(list(qs))

    ai_result = {}
    if not df.empty:
        ai_result = run_ai_pipeline(
            df,
            kpis={
                "net_result": net_result,
                "cash_balance": cash_balance,
                "expenses_30d": total_expenses / 12
            }
        )



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