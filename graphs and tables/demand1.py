import pandas as pd
import matplotlib.pyplot as plt

# Путь к файлам
vacancies_file = "vacancies_2024.csv"
exchange_rates_file = "currency.csv"

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
exchange_rates = pd.read_csv(exchange_rates_file)

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

# Приведение к формату даты без времени
php_vacancies["published_date"] = php_vacancies["published_at"].dt.date
exchange_rates["date"] = pd.to_datetime(exchange_rates["date"]).dt.date

# Присоединение курсов валют
php_vacancies = php_vacancies.merge(exchange_rates, how="left", left_on="published_date", right_on="date")

# Учитываем только вакансии с указанной зарплатой и исключаем некорректные данные
php_vacancies = php_vacancies.dropna(subset=["salary_from", "salary_to"])
php_vacancies = php_vacancies[php_vacancies["salary_from"] <= 10000000]
php_vacancies = php_vacancies[php_vacancies["salary_to"] <= 10000000]

# Функция для конвертации зарплаты в рубли
def get_salary_in_rub(row):
    currency = row["salary_currency"]
    if currency == "RUR":  # Если валюта уже в рублях, курс = 1
        return (row["salary_from"] + row["salary_to"]) / 2
    elif pd.notna(row.get(currency)):  # Проверяем, что курс валюты существует
        return (row["salary_from"] + row["salary_to"]) / 2 * row[currency]
    else:
        return None

# Применение функции для конвертации зарплаты в рубли
php_vacancies["salary_rub"] = php_vacancies.apply(get_salary_in_rub, axis=1)

# Удаляем строки с отсутствующими курсами валют
php_vacancies = php_vacancies.dropna(subset=["salary_rub"])

# Группировка по годам и расчет средней зарплаты
salary_trend = php_vacancies.groupby("year")["salary_rub"].mean().reset_index()

print(salary_trend)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(salary_trend["year"], salary_trend["salary_rub"], marker="o", linestyle="-")
plt.title("Динамика уровня зарплат по годам для PHP-программистов (в рублях)", fontsize=14)
plt.xlabel("Год", fontsize=12)
plt.ylabel("Средняя зарплата (руб.)", fontsize=12)
plt.grid(True)
plt.savefig("output/Динамика зп по годам для PHP-программистов.png")
plt.show()