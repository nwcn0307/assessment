from django.shortcuts import render
from .models import Resource

# Create your views here.
def index(request):
    resources = Resource.objects.all()
    context = {'resources':resources}

    return render(request, 'pages/index.html', context)

def about(request):
    return render(request, 'pages/about.html')