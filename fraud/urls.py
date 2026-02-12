

from django.urls import path
from . import views

app_name = "fraud"

urlpatterns = [
    path("", views.fraud_dashboard, name="dashboard"),
    path("transactions/", views.fraud_list, name="list"),
    path("transaction/<int:pk>/", views.fraud_detail, name="detail"),
    path("report/", views.fraud_report, name="report"),
]