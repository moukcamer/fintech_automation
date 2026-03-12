from django.urls import path
from .views.views import api_home, contact_api
from api.views.analytics import monthly_performance, financial_summary
from api.views.transactions import create_transaction
from api.views.fraud import fraud_check


urlpatterns = [

    path('', api_home, name='api_home'),

    path('contact/', contact_api, name='contact-api'),

    path(
        "analytics/monthly-performance/",
        monthly_performance,
        name="monthly-performance"
    ),

    path(
        "analytics/summary/",
        financial_summary,
        name="financial-summary"
    ),

    path(
        "transactions/",
        create_transaction,
        name="api-create-transaction"
    ),

    path(
        "fraud/<int:transaction_id>/",
        fraud_check,
        name="api-fraud-check"
    ),

]



urlpatterns = [



]

