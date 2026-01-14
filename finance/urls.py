from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "finance"

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
    path("invoices/", views.invoice_list, name="finance-invoices"),
    path("api/", include(router.urls)),
    path("documents/upload/", views.upload_document, name="documents-upload"),
    path("documents/", views.document_list, name="documents-list"),
]
