from django.urls import path
from . import api_views

urlpatterns = [
    path(
        "monthly-performance/",
        api_views.monthly_performance,
        name="monthly-performance"
    ),
]
