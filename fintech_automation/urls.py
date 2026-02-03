"""
URL configuration for fintech_automation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    return render(request, "index.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # PAGE D'ACCUEIL
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
    path("finance/", include(("finance.urls", "finance"), namespace="finance")),
    path("ml/", include("ml.urls")),
    path("api/analytics/", include("data_processing.api.urls")),
    path("api/analytics/", include("data_processing.analytics.urls")),
    path("api/", include("api.urls")),
    path("", include("pages.urls")),
    path("accounts/", include("django.contrib.auth.urls") ),
    path("ai/", include("ai.urls")),

]







