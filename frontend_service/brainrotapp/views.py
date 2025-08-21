from django.shortcuts import render
import aiohttp
from .forms import PromptForm, LoginForm

async def index(request):
    form = PromptForm()
    return render(request, "view.html", {"form": form})

def login(request):
    form = LoginForm()
    return render(request, 'login.html', {"form": form})

async def about_user(request):
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8001/api/users/me", cookies={"access_token": request.COOKIES.get("access_token")}) as response:
            if response.status == 200:
                return render(request, "about_user.html")
            else:
                return render(request, "login.html")
    