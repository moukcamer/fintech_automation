from rest_framework import serializers
from .models import (
    Customer,
    Account,
    Transaction,
    Invoice,
    Payment,
    Company,
    Document,
    DashboardStats
)

# ============================
# CUSTOMER
# ============================
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "created_at",
        ]


# ============================
# ACCOUNT
# ============================
class AccountSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source="customer.name")

    class Meta:
        model = Account
        fields = [
            "id",
            "name",
            "currency",
            "balance",
            "customer",
            "customer_name",
            "created_at",
        ]


# ============================
# TRANSACTION
# ============================
class TransactionSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source="account.name")
    customer_name = serializers.ReadOnlyField(source="customer.name")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "date",
            "amount",
            "transaction_type",
            "status",
            "description",
            "account",
            "account_name",
            "customer",
            "customer_name",
            "created_at",
        ]


# ============================
# INVOICE
# ============================
class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "amount",
            "status",
            "created_at",
        ]


# ============================
# PAYMENT
# ============================
class PaymentSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source="account.name")
    invoice_id = serializers.ReadOnlyField(source="invoice.id")

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "amount",
            "date",
            "account",
            "account_name",
            "invoice",
            "invoice_id",
        ]


# ============================
# COMPANY
# ============================
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "address",
            "email",
            "phone",
            "created_at",
        ]


# ============================
# DOCUMENT
# ============================
class DocumentSerializer(serializers.ModelSerializer):
    invoice_id = serializers.ReadOnlyField(source="invoice.id")
    uploaded_by_username = serializers.ReadOnlyField(source="uploaded_by.username")

    class Meta:
        model = Document
        fields = [
            "id",
            "invoice",
            "invoice_id",
            "uploaded_by",
            "uploaded_by_username",
            "file",
            "uploaded_at",
        ]


# ============================
# DASHBOARD STATS (lecture seule)
# ============================
class DashboardStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardStats
        fields = [
            "total_customers",
            "total_transactions",
            "total_balance",
            "updated_at",
        ]
        read_only_fields = fields
