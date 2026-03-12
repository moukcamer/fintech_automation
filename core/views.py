
from django.shortcuts import render, redirect
from .models import ContactMessage


def home(request):

    return render(request, "core/index.html")


def about(request):

    return render(request, "core/about.html")


def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return redirect("contact")

    return render(request, "core/contact.html")