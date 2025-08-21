from django.shortcuts import render, redirect
import requests
from .forms import PromptForm, LoginForm, RegistrationForm

async def index(request):
    form = PromptForm()
    return render(request, "view.html", {"form": form})

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {"form": form})

def about_user(request):
    access_token = request.COOKIES.get("access_token")
    if access_token:
        try:
            responce = requests.get("http://127.0.0.1:8001/api/users/me", cookies={"access_token": access_token})
            if responce.status_code == 200:
                return render(request, "about_user.html")
            else:
                return redirect("brainrotapp:login")
        except requests.exceptions.RequestException:
            return redirect("brainrotapp:login")
    else:
        return redirect("brainrotapp:login")

def register(request):
    form = RegistrationForm()
    return render(request, "registration.html", {"form": form})