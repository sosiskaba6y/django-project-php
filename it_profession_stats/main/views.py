# main/views.py

from django.shortcuts import render
from .models import Profession

def home(request):
    profession = Profession.objects.first()  # Пример, нужно доработать логику
    return render(request, 'main/home.html', {'profession': profession})