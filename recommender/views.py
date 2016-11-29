from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
from forms import RegisterForm, LoginForm


def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        form.is_valid()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        #new_user = User(email=email, password=password, user_type=user_type)
        #new_user.save() # save the new user to the database

        return redirect_user_to_homepage(new_user)
    else:
        form = RegisterForm()
    return render(request, "register.html", { "form": form })

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        form.is_valid()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Re-render the login with a failure message
            return render(request, "login.html", { "invalid_email": True, "form": blank_form })

        # Check that the passwords match
        if user.password == password:
            # Redirect the user to their home page
            return redirect_user_to_homepage(user)
        else:
            # Reject the login and notify that the password was wrong
            return render(request, "login.html", { "invalid_password": True, "form": blank_form })
        """
    else:
        form = LoginForm()
    return render(request, "login.html", { "form": form })

def demo(request):
    context = {
        'gameList': []
    }
    return render(request, "demo.html", context)
