from django.shortcuts import render
from .models import Customer, Account, Transaction, Notification, DashboardStats


def dashboard_home(request):
    stats = DashboardStats.objects.first()

    recent_transactions = Transaction.objects.order_by('-created_at')[:10]
    customers = Customer.objects.all()
    accounts = Account.objects.all()

    context = {
        "stats": stats,
        "recent_transactions": recent_transactions,
        "customers": customers,
        "accounts": accounts,
    }

    return render(request, "dashboard/dashboard_home.html", context)
