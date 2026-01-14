from django.shortcuts import render

def index(request):
    return render(request, "pages/index.html")

def fonctionnalites(request):
    return render(request, "pages/fonctionnalites.html")

def performance(request):
    return render(request, "pages/performance.html")

def contact(request):
    return render(request, "pages/contact.html")

def discover(request):
    return render(request, "pages/discover.html")

