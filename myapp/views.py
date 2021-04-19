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
import matplotlib
from matplotlib import pyplot
import numpy

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
            form = forms.ExhibitionForm2(request.POST, request.FILES)
            if form.is_valid():
                form.save(request)
                return redirect('/')
        else:
            form = forms.ExhibitionForm2()
    else:
        return redirect('/')
    context = {
        "title":"Exhibitions - View Exhibition",
        "is_staff": isStaff(request.user),
        "form": form,
    }
    return render(request, "exhibition_create.html", context=context)


def viewExhibition(request, pk):
    exhibition = models.Exhibition.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user == exhibition.student:
            isArtist = True
        else:
            isArtist = False
    else:
        isArtist = False
    works = models.ArtWork.objects.filter(exhibition=pk)
    mentors = exhibition.mentors.all()
    categories = exhibition.categories.all()
    if exhibition.degree == 'B':
        type = 'BFA'
    else:
        type = 'MFA'
    baseUrl = 'http://localhost:8000/' #'https://exhibition.csuchico.edu/'
    flyerUrl = baseUrl + exhibition.flyer.name
    emailBody =  'Check out the ' + exhibition.title + ' exhibition at Chico State: ' + baseUrl + 'exhibition/view/' + str(exhibition.pk) + '/'
    context = {
        "title":"Exhibitions -  Edit Exhibition",
        "is_staff": isStaff(request.user),
        "is_artist": isArtist,
        "exhibition": exhibition,
        "works": works,
        "type": type,
        "mentors": mentors,
        "categories": categories,
        "emailBody": emailBody,
    }
    return render(request, 'exhibition_view.html', context=context)


def updateExhibition(request, pk):
    exhibition = models.Exhibition.objects.get(pk=pk)
    if request.method == "POST":
        form = forms.ExhibitionForm2(request.POST, request.FILES, instance=exhibition)
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
    return render(request, 'exhibition_delete.html', context)

@login_required
def createArtWork(request, pk):
    '''
    Create a new ArtWork object
    '''
    exhibition = models.Exhibition.objects.get(pk=pk)
    isArtist = request.user==exhibition.student
    if isStaff(request.user) or isArtist:
        if request.method == "POST":
            form = forms.ArtForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request)
                return redirect('/')
        else:
            form = forms.ArtForm(initial={'exhibition': exhibition})
            #form.exhibition = exhibition
    else:
        return redirect('/')
    context = {
        "title":"Exhibitions - Create Artwork",
        "is_staff": isStaff(request.user),
        "is_artist": isArtist,
        "form": form,
        #"exhibition": exhibition,
    }
    return render(request, "artwork_create.html", context=context)


@login_required
def updateArtWork(request, pk):
    '''
    Create a new ArtWork object
    '''
    artwork = models.ArtWork.objects.get(pk=pk)
    print(artwork)
    #exhibition = models.Exhibition.objects.get(pk=pk)
    if isStaff(request.user):
        if request.method == "POST":
            form = forms.ArtForm(request.POST, request.FILES, instance=artwork)
            #form.exhibition = exhibition
            if form.is_valid():
                form.save(request)
                return redirect('/')
        else:
            form = forms.ArtForm(instance=artwork)
            #form.exhibition = exhibition
    else:
        return redirect('/')
    context = {
        "title": 'Exhibitions - Update Artwork',
        "is_staff": isStaff(request.user),
        "form": form,
        "artwork": artwork,
    }
    return render(request, "artwork_update.html", context=context)


def deleteArtWork(request, pk):
    artwork = models.ArtWork.objects.get(pk=pk)
    if request.method == "POST":
        artwork.delete()
        return redirect('/')
    context = {'item': artwork}
    return render(request, 'artwork_delete.html', context)


def generateDegreePieChart():
    ''' Pie Chart to illustrate ration of BFA to MFA exhibitions '''
    bfa = models.Exhibition.objects.filter(degree='B').count()
    mfa = models.Exhibition.objects.filter(degree='M').count()
    
    labels = 'BFA', 'MFA'
    sizes = bfa, mfa
    explode = (0.1, 0)
    fig1, ax1 = pyplot.subplots()
    ax1.pie(
        sizes,
        explode=explode,
        labels=labels,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90
    )
    ax1.axis('equal')
    pyplot.savefig('media/bfaMfaPieChart.png')
    fig1.clear()



def generateCategoryBarChart():
    ''' Generate bar chart for categories e.g. Ceramic, Painting, etc '''
    categories = models.Category.objects.all()
    categoryCounts = {}
    for c in categories:
        categoryCounts.update({c: models.Exhibition.objects.filter(categories=c).count()})
    pyplot.bar(
        range(len(categoryCounts)),
        list(categoryCounts.values()),
        align='center',
    )
    pyplot.xticks(
        range(len(categoryCounts)),
        categoryCounts.keys(),
        rotation=45
    )
    pyplot.gcf().subplots_adjust(bottom=0.25)
    pyplot.savefig('media/categoryBarChart.png')


def dashboard(request):
    ''' Gerenate charts for Dashboard '''
    generateDegreePieChart()
    generateCategoryBarChart()

    context = {
        "title": 'Exhibitions - Dashboard'
    }
    return render(request, "dashboard.html", context=context)


@login_required
def createMentor(request):
    if isStaff(request.user):
        if request.method == "POST":
            form = forms.MentorForm(request.POST)
            if form.is_valid():
                form.save(request)
                return redirect('/')
        else:
            form = forms.MentorForm()
    else:
        return redirect('/')
    context = {
        "title":"Exhibitions - New Mentor",
        "is_staff": isStaff(request.user),
        "form": form,
    }
    return render(request, "mentor_create.html", context=context)


@login_required
def createCategory(request):
    if isStaff(request.user):
        if request.method == "POST":
            form = forms.CategoryForm(request.POST)
            if form.is_valid():
                form.save(request)
                return redirect('/')
        else:
            form = forms.CategoryForm()
    else:
        return redirect('/')
    context = {
        "title":"Exhibitions - New Category",
        "is_staff": isStaff(request.user),
        "form": form,
    }
    return render(request, "category_create.html", context=context)