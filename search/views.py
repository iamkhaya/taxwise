from django.shortcuts import render
from django.http import HttpResponse

from search.models import Tarriff

def index(request):
    tarriffs = Tarriff.objects.all()
    return render(request, 'search/index.html', {
        'tarriffs': tarriffs,
    })
