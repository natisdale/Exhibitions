#from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from . import models
#from . import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
import json

def index(request):
    context = {
        "title":"Exhibitions",
        "author":"Nathan Tisdale",
        "description":"BFA & MFA Exhibitions",
        "keywoards":"CINS490, html, css, python, django, vue.js",
        "body":"template body",}
    return render(request, "index.html", context=context)

def logout_view(request):
    logout(request)
    return redirect("/")