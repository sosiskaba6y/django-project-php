# main/views.py
import requests
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

def latest_vacancies(request):
    keywords = ['php', 'пхп', 'рнр']
    text_query = ' OR '.join(keywords)
    url = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'HH-User-Agent'  # Стандартный User-Agent
    }
    params = {
        'text': text_query,
        'per_page': 10,
        'only_with_salary': True,
        'date_from': 'now-1d',  # Вакансии за последние 24 часа
        'order_by': 'publication_time',
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        vacancies = response.json().get('items', [])
        for vacancy in vacancies:
            # Получаем полное описание вакансии
            vacancy_details_response = requests.get(vacancy['url'], headers=headers)
            if vacancy_details_response.status_code == 200:
                vacancy_details = vacancy_details_response.json()

                # Получаем навыки
                key_skills = ', '.join([skill['name'] for skill in vacancy_details.get('key_skills', [])])

                # Формируем оклад
                if vacancy['salary']:
                    salary_from = vacancy['salary'].get('from', None)
                    salary_to = vacancy['salary'].get('to', None)
                    currency = vacancy['salary'].get('currency', 'RUB')
                    if salary_from and salary_to:
                        vacancy['salary_str'] = f'{salary_from} - {salary_to} {currency}'
                    elif salary_from:
                        vacancy['salary_str'] = f'от {salary_from} {currency}'
                    elif salary_to:
                        vacancy['salary_str'] = f'до {salary_to} {currency}'
                    else:
                        vacancy['salary_str'] = 'Не указано'
                else:
                    vacancy['salary_str'] = 'Не указано'

                # Обновляем поля вакансии
                vacancy['description'] = vacancy_details.get('description', '')
                vacancy['key_skills'] = key_skills
                vacancy['company'] = vacancy_details.get('employer', {}).get('name', 'Неизвестно')
                vacancy['region'] = vacancy_details.get('area', {}).get('name', 'Неизвестно')
                vacancy['published_at'] = vacancy_details.get('published_at', '')

        return render(request, 'main/latest_vacancies.html', {'vacancies': vacancies})
    else:
        return render(request, 'main/latest_vacancies.html', {'error': 'Ошибка при получении данных'})