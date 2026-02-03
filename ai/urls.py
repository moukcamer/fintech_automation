# ai/urls.py

from django.urls import path
from .views import anomaly_detection, cashflow_forecast, ai_report_pdf

urlpatterns = [
    path("anomalies/", anomaly_detection, name="anomaly_detection"),
    path("forecast/cashflow/", cashflow_forecast, name="cashflow_forecast"),
    path("report/pdf/", ai_report_pdf, name="ai_report_pdf"),

]
