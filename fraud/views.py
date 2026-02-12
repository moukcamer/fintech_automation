from django.contrib import admin
from .models import Transaction
from django.shortcuts import render
from django.db.models import Count

# ===============================
# LISTE DES TRANSACTIONS
# ===============================
def fraud_list(request):
    transactions = Transaction.objects.all().order_by("-created_at")

    context = {
        "transactions": transactions
    }
    return render(request, "fraud/list.html", context)


# ===============================
# DETAIL TRANSACTION
# ===============================
def fraud_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    return render(request, "fraud/detail.html", {
        "transaction": transaction
    })

def fraud_dashboard(request):
    transactions = Transaction.objects.all().order_by("-timestamp")[:20]
    return render(request, "fraud/dashboard.html", {"transactions": transactions})


def fraud_report(request):

    total = Transaction.objects.count()
    normal = Transaction.objects.filter(status="normal").count()
    suspect = Transaction.objects.filter(status="suspect").count()
    fraud = Transaction.objects.filter(status="fraud").count()

    high_risk = Transaction.objects.filter(status="fraud").order_by("-risk_score")[:10]

    return render(request, "fraud/report.html", {
        "total": total,
        "normal": normal,
        "suspect": suspect,
        "fraud": fraud,
        "high_risk": high_risk
    })
