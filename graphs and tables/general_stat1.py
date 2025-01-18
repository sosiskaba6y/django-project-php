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

# Удаление строк с некорректной датой
vacancies = vacancies.dropna(subset=["published_at"])

# Приведение к формату даты без времени
vacancies["published_date"] = vacancies["published_at"].dt.date
exchange_rates["date"] = pd.to_datetime(exchange_rates["date"]).dt.date

# Присоединение курсов валют
vacancies = vacancies.merge(exchange_rates, how="left", left_on="published_date", right_on="date")

# Учитываем только вакансии с указанной зарплатой и исключаем некорректные данные
vacancies = vacancies.dropna(subset=["salary_from", "salary_to"])
vacancies = vacancies[vacancies["salary_from"] <= 10_000_000]
vacancies = vacancies[vacancies["salary_to"] <= 10_000_000]

# Удаление вакансий с отсутствующими курсами валют
def get_salary_in_rub(row):
    currency = row["salary_currency"]
    if currency == "RUR":  # Если валюта уже в рублях, курс = 1
        return (row["salary_from"] + row["salary_to"]) / 2
    elif pd.notna(row.get(currency)):  # Проверяем, что курс валюты существует
        return (row["salary_from"] + row["salary_to"]) / 2 * row[currency]
    else:
        return None

vacancies["salary_rub"] = vacancies.apply(get_salary_in_rub, axis=1)
vacancies = vacancies.dropna(subset=["salary_rub"])  # Удаляем строки с отсутствующими курсами валют

# Группировка по годам и расчет средней зарплаты
vacancies["year"] = vacancies["published_at"].dt.year
salary_trend = vacancies.groupby("year")["salary_rub"].mean().reset_index()

print(salary_trend)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(salary_trend["year"], salary_trend["salary_rub"], marker="o", linestyle="-")
plt.title("Динамика уровня зарплат по годам (в рублях)", fontsize=14)
plt.xlabel("Год", fontsize=12)
plt.ylabel("Средняя зарплата (руб.)", fontsize=12)
plt.grid(True)
plt.savefig("output/Динамика зп по годам.png")
plt.show()
