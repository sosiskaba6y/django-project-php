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

# Приведение к формату даты без времени
vacancies["published_date"] = vacancies["published_at"].dt.date
exchange_rates["date"] = pd.to_datetime(exchange_rates["date"]).dt.date

# Присоединение курсов валют
vacancies = vacancies.merge(exchange_rates, how="left", left_on="published_date", right_on="date")

# Учитываем только вакансии с указанной зарплатой и исключаем некорректные данные
vacancies = vacancies.dropna(subset=["salary_from", "salary_to"])
vacancies = vacancies[vacancies["salary_from"] <= 10000000]
vacancies = vacancies[vacancies["salary_to"] <= 10000000]

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
vacancies["salary_rub"] = vacancies.apply(get_salary_in_rub, axis=1)

# Удаляем строки с отсутствующими курсами валют
vacancies = vacancies.dropna(subset=["salary_rub"])

# Группировка по городам и расчет средней зарплаты
salary_by_city = vacancies.groupby("area_name")["salary_rub"].mean().reset_index()

# Сортировка по средней зарплате в порядке убывания
salary_by_city = salary_by_city.sort_values(by="salary_rub", ascending=False)

# Оставляем только топ N городов, остальные объединяем в "Другие"
top_n = 20  # Количество городов для отображения
top_cities = salary_by_city.head(top_n)
other_cities_mean = salary_by_city["salary_rub"][top_n:].mean()
other_cities = pd.DataFrame({"area_name": ["Другие"], "salary_rub": [other_cities_mean]})

# Объединяем топ города и "Другие" города
final_salary_data = pd.concat([top_cities, other_cities])

print(final_salary_data)

# Построение графика
plt.figure(figsize=(12, 8))
plt.barh(final_salary_data["area_name"], final_salary_data["salary_rub"], color='skyblue')
plt.title(f"Уровень зарплат по городам для всех профессий (в порядке убывания), ТОП-{top_n} + Другие", fontsize=14)
plt.xlabel("Средняя зарплата (руб.)", fontsize=12)
plt.ylabel("Город", fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("output/Уровень зарплат по городам для всех профессий_top10_and_others.png")
plt.show()