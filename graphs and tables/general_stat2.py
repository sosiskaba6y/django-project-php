import pandas as pd

# Путь к файлу с вакансиями
vacancies_file = "vacancies_2024.csv"

# Загрузка данных
vacancies = pd.read_csv(vacancies_file, dtype={
    "name": str,
    "key_skills": str,
    "salary_from": float,
    "salary_to": float,
    "salary_currency": str,
    "area_name": str,
    "published_at": str
})

# Приведение столбца published_at к формату datetime
vacancies["published_at"] = pd.to_datetime(vacancies["published_at"], errors="coerce", utc=True)

# Удаление строк с некорректной датой (если необходимо)
# vacancies = vacancies.dropna(subset=["published_at"])

# Извлечение года из даты публикации
vacancies["year"] = vacancies["published_at"].dt.year

# Группировка по году и подсчет количества вакансий
vacancy_count_by_year = vacancies.groupby("year").size().reset_index(name='count')

print(vacancy_count_by_year)

# Построение графика
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(vacancy_count_by_year["year"], vacancy_count_by_year["count"], color='skyblue')
plt.title("Количество вакансий по годам", fontsize=14)
plt.xlabel("Год", fontsize=12)
plt.ylabel("Количество вакансий", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig("output/Количество вакансий по годам.png")
plt.show()