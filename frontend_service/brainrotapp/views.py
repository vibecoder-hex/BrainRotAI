from django.shortcuts import render, redirect
import requests
from .forms import PromptForm, LoginForm, RegistrationForm
from .check_auth import is_authenticate

def index(request):
    form = PromptForm()
    return render(request, "view.html", {"form": form})

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {"form": form})

def about_user(request):
    access_token = request.COOKIES.get("access_token")
    if not is_authenticate(access_token):
        return redirect('brainrotapp:login')
    return render(request, 'about_user.html')
    

def register(request):
    form = RegistrationForm()
    return render(request, "registration.html", {"form": form})