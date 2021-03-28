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

def isStaff(user):
    return user.is_staff

def index(request):
    is_staff = False
    if request.user.is_authenticated:
        if isStaff(request.user):
            exhibitions = models.Exhibition.objects.all()
            is_staff = True
        else:
            exhibitions = models.Exhibition.objects.filter(student=request.user)
    else:
        exhibitions = models.Exhibition.objects.filter(public=True)
    context = {
        "title":"Exhibitions",
        "author":"Nathan Tisdale",
        "description":"BFA & MFA Exhibitions",
        "keywords":"CINS490, html, css, python, django, vue.js",
        "body":"template body",
        "is_staff":is_staff,
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


def getExhibitions(request):
    if not request.user.is_authenticated:
        resultSet = models.Exhibition.objects.filter(public=True).order_by('startDate').reverse()
    else:
        if request.user.is_staff:
            resultSet = models.Exhibition.objects.all().order_by('startDate').reverse()
        else:
            resultSet = models.Exhibition.objects.filter(student=request.user)
    exhibitionList = {}
    exhibitionList["exhibitions"] = []
    for result in resultSet:
        temp = {}
        temp["id"] = result.id
        temp["title"] = result.title
        temp["student"] = result.student.first_name + ' ' + result.student.last_name
        temp["startDate"] = result.startDate
        temp["endDate"] = result.endDate
        temp["flyer"] = result.flyer.url
        exhibitionList["exhibitions"] += [temp]
    return JsonResponse(exhibitionList)


@login_required
def createExhibition(request):
    if isStaff(request.user):
        if request.method == "POST":
            form = forms.ExhibitionForm(request.POST)
            if form.is_valid():
                form.save(request)
                return redirect('/')
        else:
            form = forms.ExhibitionForm()
    else:
        redirect('/')
    context = {
        "title":"Exhibition",
        "is_staff": isStaff(request.user),
        "form": form,
    }
    return render(request, "exhibition_create.html", context=context)


def viewExhibition(request, pk):
    exhibition = models.Exhibition.objects.get(pk=pk)
    works = models.ArtWork.objects.filter(exhibition=pk)
    if exhibition.degree == 'B':
        type = 'BFA'
    else:
        type = 'MFA'
    context = {
        "title":"Edit Exhibition",
        "is_staff": isStaff(request.user),
        "exhibition": exhibition,
        "works": works,
        "type": type,
    }
    return render(request, 'exhibition_view.html', context=context)


def updateExhibition(request, pk):
    exhibition = models.Exhibition.objects.get(pk=pk)
    if request.method == "POST":
        form = forms.ExhibitionForm2(request.POST, instance=exhibition)
        if form.is_valid():
                form.save(request)
                return redirect('/')
    else:
        form = forms.ExhibitionForm2(instance=exhibition)
    context = {
        "title":"Edit Exhibition",
        "is_staff": isStaff(request.user),
        "form": form,
    }
    return render(request, 'exhibition_update.html', context=context)

def deleteExhibition(request, pk):
    exhibition = models.Exhibition.objects.get(pk=pk)
    if request.method == "POST":
        exhibition.delete()
        return redirect('/')
    context = {'item': exhibition}
    return render(request, 'delete.html', context)
