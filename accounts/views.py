
from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")   # redirection automatique
        else:
            messages.error(request, "Identifiants incorrects")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


# -------- REGISTER --------

def register_view(request):

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        user = form.save()

        login(request, user)

        return redirect('dashboard')

    return render(request, "accounts/register.html", {"form": form})


