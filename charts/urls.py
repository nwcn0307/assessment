from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('charts', views.charts, name='charts'),
]