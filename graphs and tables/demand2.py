import pandas as pd
import matplotlib.pyplot as plt

# Путь к файлу с вакансиями
vacancies_file = "vacancies_2024.csv"

# Загрузка данных
vacancies = pd.read_csv(vacancies_file)

# Приведение столбца published_at к формату datetime
vacancies["published_at"] = pd.to_datetime(vacancies["published_at"], errors="coerce", utc=True)

# Удаление строк с некорректной датой (если необходимо)
vacancies = vacancies.dropna(subset=["published_at"])

# Извлечение года из даты публикации
vacancies["year"] = vacancies["published_at"].dt.year

# Функция для фильтрации вакансий по профессии PHP-программист
def is_php_programmer(name, key_skills):
    search_terms = ['php', 'пхп', 'рнр']
    if any(term.lower() in name.lower() for term in search_terms):
        return True
    if pd.notna(key_skills) and any(term.lower() in key_skills.lower() for term in search_terms):
        return True
    return False

# Фильтрация данных по профессии PHP-программист
vacancies['is_php_programmer'] = vacancies.apply(lambda row: is_php_programmer(row['name'], row['key_skills']), axis=1)
php_vacancies = vacancies[vacancies['is_php_programmer']]

# Группировка по году и подсчет количества вакансий
vacancy_count_by_year = php_vacancies.groupby("year").size().reset_index(name='count')

print(vacancy_count_by_year)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(vacancy_count_by_year["year"], vacancy_count_by_year["count"], marker="o", linestyle="-")
plt.title("Динамика количества вакансий по годам для PHP-программистов", fontsize=14)
plt.xlabel("Год", fontsize=12)
plt.ylabel("Количество вакансий", fontsize=12)
plt.grid(True)
plt.savefig("output/Динамика количества вакансий по годам для PHP-программистов.png")
plt.show()