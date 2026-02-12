from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Account, Transaction
from .serializers import (
    CustomerSerializer,
    AccountSerializer,
    TransactionSerializer
)

class CustomerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Account.objects.select_related("customer")
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.select_related("account", "customer")
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
