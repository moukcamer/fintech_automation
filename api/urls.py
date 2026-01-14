from django.urls import path
from api.views.analytics import monthly_performance

app_name = "api"

urlpatterns = [
    path(
        "analytics/monthly-performance/",
        monthly_performance,
        name="monthly-performance"
    ),
]
