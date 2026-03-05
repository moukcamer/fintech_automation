from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard,  name="dashboard"), 
    path("export-report/", views.export_report, name="export_report"),  
]
