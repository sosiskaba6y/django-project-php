# main/views.py

from django.shortcuts import render
from stats.models import PageContent, PageCategory

def home(request):
    return render(request, 'main/home.html')

def generalinfo(request):
    try:
        category = PageCategory.objects.get(name='Общая статистика')
        contents = PageContent.objects.filter(category=category)
    except PageCategory.DoesNotExist:
        contents = []
    return render(request, 'main/generalinfo.html', {'contents': contents})

def demand(request):
    try:
        category = PageCategory.objects.get(name='Востребованность')
        contents = PageContent.objects.filter(category=category)
    except PageCategory.DoesNotExist:
        contents = []
    return render(request, 'main/demand.html', {'contents': contents})

def geography(request):
    try:
        category = PageCategory.objects.get(name='География')
        contents = PageContent.objects.filter(category=category)
    except PageCategory.DoesNotExist:
        contents = []
    return render(request, 'main/geography.html', {'contents': contents})

def skills(request):
    try:
        category = PageCategory.objects.get(name='Навыки')
        contents = PageContent.objects.filter(category=category)
    except PageCategory.DoesNotExist:
        contents = []
    return render(request, 'main/skills.html', {'contents': contents})

def latest_vacancies(request):
    # Пока что ничего не делаем для этой страницы
    return render(request, 'main/latest_vacancies.html')