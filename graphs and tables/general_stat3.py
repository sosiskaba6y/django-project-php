import pandas as pd

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

print(salary_by_city)

# Построение графика
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.bar(salary_by_city["area_name"], salary_by_city["salary_rub"], color='skyblue')
plt.title("Уровень зарплат по городам (в порядке убывания)", fontsize=14)
plt.xlabel("Город", fontsize=5)
plt.ylabel("Средняя зарплата (руб.)", fontsize=12)
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("output/Уровень зарплат по городам3.png")
plt.show()