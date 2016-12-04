from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from requests.auth import HTTPBasicAuth
from forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login


def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.is_valid()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        goto = form.cleaned_data["goto"]

        new = User.objects.create_user(username=username, password=password)
        new.save()

        user = authenticate(username=username, password=password)
        auth_login(request, user)

        path = "/recommender/demo" if goto == "D" else "/recommender/main"
        return HttpResponseRedirect(path)
    else:
        form = RegisterForm()
    return render(request, "register.html", { "form": form })

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form.is_valid()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        goto = form.cleaned_data["goto"]

        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            path = "/recommender/demo" if goto == "D" else "/recommender/main"
            return HttpResponseRedirect(path)
        else:
            return render(request, "login.html", { "invalid_password": True, "form": blank_form })
    else:
        form = LoginForm()
    return render(request, "login.html", { "form": form })

def demo(request):
    context = {
        'username': request.user.username
    }
    return render(request, "demo.html", context)

def main(request):
    context = {
        'username': request.user.username
    }
    return render(request, "main.html", context)
