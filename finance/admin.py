from django.contrib import admin
from .models import (
    Customer,
    Account,
    Transaction,
    Invoice,
    Payment,
    Company,
    Document,
    DashboardStats,
)

# ==========================
# CUSTOMER
# ==========================
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "customer_number",
        "first_name",
        "last_name",
        "email",
        "country",
        "city",
        "created_at",
    )
    search_fields = (
        "customer_number",
        "first_name",
        "last_name",
        "email",
    )
    ordering = ("last_name", "first_name")


# ==========================
# ACCOUNT
# ==========================
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_number",
        "customer",
        "account_type",
        "currency",
        "balance",
        "status",
        "created_at",
    )
    search_fields = (
        "account_number",
        "customer__customer_number",
    )
    list_filter = ("account_type", "currency", "status")
    ordering = ("account_number",)


# ==========================
# TRANSACTION
# ==========================
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_ref",
        "transaction_date",
        "account",
        "transaction_type",
        "amount",
        "currency",
        "channel",
        "country",
    )
    search_fields = (
        "transaction_ref",
        "account__account_number",
    )
    list_filter = (
        "transaction_type",
        "currency",
        "channel",
        "country",
    )
    ordering = ("-transaction_date",)


# ==========================
# INVOICE
# ==========================
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "amount",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    ordering = ("-created_at",)


# ==========================
# PAYMENT
# ==========================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_type",
        "amount",
        "account",
        "invoice",
        "date",
    )
    list_filter = ("payment_type",)
    ordering = ("-date",)


# ==========================
# COMPANY
# ==========================
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "created_at",
    )
    search_fields = ("name",)


# ==========================
# DOCUMENT
# ==========================
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "invoice",
        "uploaded_by",
        "uploaded_at",
    )
    ordering = ("-uploaded_at",)


# ==========================
# DASHBOARD STATS
# ==========================
@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    list_display = (
        "total_customers",
        "total_transactions",
        "total_balance",
        "updated_at",
    )
    readonly_fields = list_display
    ordering = ("-updated_at",)
