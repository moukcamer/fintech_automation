from django.contrib import admin
from .models import Company, Account, Transaction, Invoice, Payment, Document, Notification, DashboardStats


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
    list_display = ["account", "transaction_type", "amount", "description", "created_at"]
    list_filter = ["transaction_type", "created_at"]
    search_fields = ["description"]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "company", "issued_to", "total_amount", "status", "issued_at"]
    list_filter = ["status", "issued_at"]
    search_fields = ["invoice_number", "issued_to"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "amount", "payment_types", "date"]
    list_filter = ["payment_types", "date"]
    search_fields = ["invoice__invoice_number"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "uploaded_by", "file", "uploaded_at"]
    list_filter = ["uploaded_at"]
    search_fields = ["invoice__invoice_number"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["customer", "message", "is_read", "created_at"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["customer__user__username", "message"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    list_display = ["total_customers", "total_transactions", "total_balance", "updated_at"]
    list_filter = ["updated_at"]
    search_fields = ["total_customers", "total_transactions", "total_balance"]
    readonly_fields = ["updated_at"]
    ordering = ["-updated_at"]
