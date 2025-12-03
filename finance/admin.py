from django.contrib import admin
from .models import Company, Account, Transaction, Invoice, Payment, Document


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "address", "created_at"]
    search_fields = ["name", "email", "phone"]
    list_filter = ["created_at"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "account_type", "balance", "company", "created_at"]
    list_filter = ["account_type", "company"]
    search_fields = ["name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["account", "transaction_type", "amount", "description", "date"]
    list_filter = ["transaction_type", "date"]
    search_fields = ["description"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "company", "issued_to", "total_amount", "status", "issued_at"]
    list_filter = ["status", "issued_at"]
    search_fields = ["invoice_number", "issued_to"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "amount", "payment_method", "date"]
    list_filter = ["payment_method", "date"]
    search_fields = ["invoice__invoice_number"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "uploaded_by", "file", "uploaded_at"]
    list_filter = ["uploaded_at"]
    search_fields = ["invoice__invoice_number"]
