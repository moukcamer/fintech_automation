from django.urls import path
from . import views

urlpatterns = [
    path("kpis/", views.kpis),
    path("monthly-performance/", views.monthly_performance),
    path("top-clients/", views.top_clients),
]
