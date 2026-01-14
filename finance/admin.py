from django.contrib import admin
from .models import Company, Account, Transaction, Invoice, Payment, Document, DashboardStats



# =========================
# ACCOUNT ADMIN
# =========================
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "balance",
    )
    search_fields = ("name",)
    ordering = ("name",)


# =========================
# INVOICE ADMIN
# =========================
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "customer_email",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("customer_name", "customer_email")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"


# =========================
# PAYMENT ADMIN
# =========================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice",
        "account",
        "amount",
        "date",
        "payment_type",
    )
    list_filter = ("date", "account", "payment_type")
    search_fields = ("invoice__customer_name", "account__name")
    ordering = ("-date",)
    date_hierarchy = "date"



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "address", "created_at"]
    search_fields = ["name", "email", "phone"]
    list_filter = ["created_at"]



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["account", "transaction_type", "amount", "description", "created_at"]
    list_filter = ["transaction_type", "created_at"]
    search_fields = ["description"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "uploaded_by", "file", "uploaded_at"]
    list_filter = ["uploaded_at"]
    search_fields = ["invoice__invoice_number"]


@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    list_display = ["total_customers", "total_transactions", "total_balance", "updated_at"]
    list_filter = ["updated_at"]
    search_fields = ["total_customers", "total_transactions", "total_balance"]
    readonly_fields = ["updated_at"]
    ordering = ["-updated_at"]
