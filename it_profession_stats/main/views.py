# main/views.py

from django.shortcuts import render
from stats.models import PageContent

def home(request):
    return render(request, 'main/home.html')

def generalinfo(request):
    content = PageContent.objects.filter(title='Общая статистика').first()
    return render(request, 'main/generalinfo.html', {'content': content})

def demand(request):
    content = PageContent.objects.filter(title='Востребованность').first()
    return render(request, 'main/demand.html', {'content': content})

def geography(request):
    content = PageContent.objects.filter(title='География').first()
    return render(request, 'main/geography.html', {'content': content})

def skills(request):
    content = PageContent.objects.filter(title='Навыки').first()
    return render(request, 'main/skills.html', {'content': content})

def latest_vacancies(request):
    # Пока что ничего не делаем для этой страницы
    return render(request, 'main/latest_vacancies.html')