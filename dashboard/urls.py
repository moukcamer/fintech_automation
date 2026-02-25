from django.urls import path
from .views import dashboard, monthly_transactions, transaction_types, top_accounts

app_name = "dashboard"

urlpatterns = [
    path("", dashboard,  name="dashboard"), 
    path("api/monthly/", monthly_transactions, name="monthly_transactions"),
    path("api/types/", transaction_types, name="transaction_types"),
    path("api/top-accounts/", top_accounts, name="top_accounts"),   
]
