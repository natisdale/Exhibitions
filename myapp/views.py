import os
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
from .filters import ExhibitionFilter


def isStaff(user):
    return user.is_staff

def index(request):
    is_staff = False
    if request.user.is_authenticated:
        if isStaff(request.user):
            exhibitions = models.Exhibition.objects.all()[:8]
            is_staff = True
        else:
            exhibitions = models.Exhibition.objects.filter(student=request.user)[:8]
    else:
        exhibitions = models.Exhibition.objects.filter(public=True)[:8]
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
        shadow=False,
        startangle=90
    )
    ax1.axis('equal')

    if 'WEBSITE_HOSTNAME' in os.environ: # Running on Azure
        # imageStream = BytesIO()
        # pyplot.savefig(imageStream)
        # # reset stream's position to 0
        # imageStream.seek(0)
        # # upload in blob storage
        # # blobSasUrl = os.environ['AZURE_BLOB_SAS_URL']
        # # containerClient = ContainerClient.from_container_url(blobSasUrl)
        # # blobClient = containerClient.get_blob_client(blob = "bfaMfaPieChart.png")
        # # blobClient.upload_blob(image_stream.read(), blob_type="BlockBlob") 
        # connectionString = os.environ['AZURE_CONNECT_STRING']
        # containerName = os.environ['AZURE_MEDIA_CONTAINER']
        # blobClient = BlobClient.from_connection_string(
        #     conn_str=connectionString,
        #     containter_name=containerName,
        #     blob_name="bfaMfaPieChart.png"
        # )
        # blobclient.upload(imageStream.read())
        pass
    else:
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

    if 'WEBSITE_HOSTNAME' in os.environ: # Running on Azure
        # imageStream = BytesIO()
        # pyplot.savefig(imageStream)
        # # reset stream's position to 0
        # imageStream.seek(0)
        # # upload in blob storage
        # # blobSasUrl = os.environ['AZURE_BLOB_SAS_URL']
        # # containerClient = ContainerClient.from_container_url(blobSasUrl)
        # # blobClient = containerClient.get_blob_client(blob = "categoryBarChart.png")
        # # blobCclient.upload_blob(image_stream.read(), blob_type="BlockBlob")
        # connectionString = os.environ['AZURE_CONNECT_STRING']
        # containerName = os.environ['AZURE_MEDIA_CONTAINER']
        # blobClient = BlobClient.from_connection_string(
        #     conn_str=connectionString,
        #     containter_name=containerName,
        #     blob_name="bfaMfaPieChart.png"
        # )
        # blobclient.upload(imageStream.read())
        pass
    else:
        pyplot.savefig('media/categoryBarChart.png')


def getMediaUrl():
    if 'WEBSITE_HOSTNAME' in os.environ: # Running on Azure
        return 'https://exhibitions.blob.core.windows.net/media/'
    else:
        return '/'


# def dashboard(request):
#     degrees = {}
#     labels = []
#     data = []
#     total = 0

#     resultset = models.Exhibition.objects.all()
#     for e in resultset:
#         total += 1
#         if e.degree not in degrees:
#             degrees[e.degree] = 1
#         else:
#             degrees[e.degree] += 1
        
#     for d in degrees:
#         labels.append(d)
#         data.append(int(degrees[d] / total))

#     context = {
#         "title": 'Exhibitions - Dashboard',
#         "labels": labels,
#         "data": data,
#     }
#     return render(request, "dashboard.html", context=context)

def dashboard(request):
    ''' Gerenate charts for Dashboard '''
    # generateDegreePieChart()
    # generateCategoryBarChart()

    context = {
        "title": 'Exhibitions - Dashboard',
        "location": getMediaUrl()
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


def filter(request):
    is_staff = False
    exhibitions = models.Exhibition.objects.filter(public=True)
    exhibitionFilter = ExhibitionFilter(request.GET, queryset=exhibitions)
    exhibitions = exhibitionFilter.qs
    context = {
        "title":"Exhibitions - Filter",
        "author":"Nathan Tisdale",
        "description":"BFA & MFA Exhibitions",
        "keywords":"CINS490, html, css, python, django, vue.js",
        "body":"template body",
        "is_staff":is_staff,
        "exhibitions":exhibitions,
        "exhibitionFilter":exhibitionFilter,
    }
    return render(request, "filter.html", context=context)

def degreePieChart(request):
    '''
    Adapted from https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    '''
    labels = [ 'bfa', 'mfa' ]
    counts = {
        'B': 0,
        'M': 0,
    }
    exhibitions = models.Exhibition.objects.filter(public=True)
    for e in exhibitions:
        counts[e.degree] +=1
    
    data = [ counts['B'], counts['M'] ]

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def yearsBarChart(request):
    '''
    Adapted from https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    '''
    labels = []
    counts = {}
    data = []
    exhibitions = models.Exhibition.objects.filter(public=True)
    for e in exhibitions:
        counts[e.startDate.year] = 0
    for e in exhibitions:
        counts[e.startDate.year] +=1
    for y in counts:
        labels.append(y)
        data.append(counts[y])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


def categoryChart(request):
    '''
    Adapted from https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
    '''
    labels = []
    counts = {}
    data = []
    categories = models.Category.objects.all()
    for c in categories:
        counts[c.name] = models.Exhibition.objects.filter(categories__name__contains=c.name).count()
    for c in counts:
        labels.append(c)
        data.append(counts[c])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
