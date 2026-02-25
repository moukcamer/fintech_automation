from django.contrib import admin
from .models import (
    Customer,
    Account,
    Transaction,
    Invoice,
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
        "name",
        "account_type",
        "currency",
        "balance",
        
    )
    search_fields = (
        "account_number",
        "name",
    )
    list_filter = ("account_type", "currency", "status")



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    # Colonnes affichées dans la liste
    list_display = (
        "transaction_ref",
        "account",
        "amount",
        "transaction_type",
        "status",
        "is_fraud",
        "fraud_probability",
        "created_at",
        "is_posted",
    )

    # Filtres à droite
    list_filter = (
        "transaction_type",
        "channel",
        "status",
        "is_fraud",
        "is_posted",
        
    )

    # Champs non modifiables
    readonly_fields = (
        "transaction_ref",
        "created_at",
        "fraud_probability",
        "risk_fraud",
        "ai_status",
        "created_at",
    )

 

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
