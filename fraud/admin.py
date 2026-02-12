from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "status", "risk_score", "timestamp")
    list_filter = ("status", "timestamp")
    search_fields = ("user__email", "ip_address")

