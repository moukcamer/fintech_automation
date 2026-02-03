#ml/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services import forecast_payments


@login_required
def financial_forecast_view(request):
    forecast = forecast_payments(months_ahead=6)

    return render(
        request,
        "ml/forecast.html",
        {"forecast": forecast}
    )
