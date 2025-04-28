
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from crud import export_all_data, import_all_data, clear_database, import_data, export_data

def charts(request):

        return render(request,'charts/charts.html')