#from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import models
from . import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
import json

def isStudent(user):
    return user.groups.filter(name="Students").exists()

def index(request):
    if request.user.is_authenticated:
        if isStudent(request.user):
            exhibitions = models.Exhibition.objects.all()
        else:
            exhibitions = models.Exhibition.objects.filter(student=request.user)
    else:
        exhibitions = models.Exhibition.objects.filter(public=True)
    context = {
        "title":"Exhibitions",
        "author":"Nathan Tisdale",
        "description":"BFA & MFA Exhibitions",
        "keywoards":"CINS490, html, css, python, django, vue.js",
        "body":"template body",
        "exhibitions":exhibitions,
    }
    return render(request, "index.html", context=context)


def logout_view(request):
    logout(request)
    return redirect("/")


def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "register.html", context=context)
