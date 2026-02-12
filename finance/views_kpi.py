from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Transaction, Customer, Account

class DashboardKPI(APIView):
    def get(self, request):
        return Response({
            "total_customers": Customer.objects.count(),
            "total_accounts": Account.objects.count(),
            "total_transactions": Transaction.objects.count(),
            "total_income": Transaction.objects.filter(
                transaction_type="IN"
            ).aggregate(Sum("amount"))["amount__sum"] or 0,
            "total_expenses": Transaction.objects.filter(
                transaction_type="OUT"
            ).aggregate(Sum("amount"))["amount__sum"] or 0,
        })
