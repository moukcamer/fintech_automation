from rest_framework import serializers
from .models import (
    Company,
    Account,
    Transaction,
    Invoice,
    Payment,
    Document
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"



class TransactionSerializer(serializers.ModelSerializer):
    account_name = serializers.ReadOnlyField(source="account.name")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "account_name",
            "amount",
            "transaction_type",
            "description",
            "date",
        ]



class InvoiceSerializer(serializers.ModelSerializer):
    company_name = serializers.ReadOnlyField(source="company.name")
    documents = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "company",
            "company_name",
            "issued_to",
            "total_amount",
            "status",
            "issued_at",
            "documents",
        ]

    def get_documents(self, obj):
        return [doc.file.url for doc in obj.documents.all()]


class PaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.ReadOnlyField(source="invoice.invoice_number")

    class Meta:
        model = Payment
        fields = [
            "id",
            "invoice",
            "invoice_number",
            "amount",
            "payment_method",
            "date",
        ]


class DocumentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.ReadOnlyField(source="invoice.invoice_number")
    uploaded_by_username = serializers.ReadOnlyField(source="uploaded_by.username")

    class Meta:
        model = Document
        fields = [
            "id",
            "invoice",
            "invoice_number",
            "uploaded_by",
            "uploaded_by_username",
            "file",
            "uploaded_at",
        ]
