from django.urls import path
from .views import financial_forecast_view

app_name = "ml"

urlpatterns = [
    path("forecast/", financial_forecast_view, name="forecast"),
]
