from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"companies", views.CompanyViewSet)
router.register(r"accounts", views.AccountViewSet)
router.register(r"transactions", views.TransactionViewSet)
router.register(r"invoices", views.InvoiceViewSet)
router.register(r"payments", views.PaymentViewSet)
router.register(r"documents", views.DocumentViewSet)

urlpatterns = [
    # HTML pages
    path("", views.dashboard, name="finance_dashboard"),
    path("accounts/", views.account_list, name="account_list"),
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("invoices/", views.invoice_list, name="invoice_list"),

    # API
    path("api/", include(router.urls)),
]
