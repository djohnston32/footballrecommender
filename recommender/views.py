from django.shortcuts import render
from django.http import HttpResponse

import requests
from requests.auth import HTTPBasicAuth


def index(request):
    return render(request, "index.html")

def demo(request):
    context = {
        'gameList': []
    }
    return render(request, "demo.html", context)
