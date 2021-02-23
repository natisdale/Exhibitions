#from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {
        "title":"Exhibitions",
        "body":"template body",}
    return render(request, "index.html", context=context)
