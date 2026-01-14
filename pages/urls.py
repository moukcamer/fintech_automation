
from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("discover/", views.discover, name="discover"),
    path("contact/", views.contact, name="contact"),
    path("performance/", views.performance, name="performance"),
    path("fonctionnalites/", views.fonctionnalites, name="fonctionnalites"),
]
