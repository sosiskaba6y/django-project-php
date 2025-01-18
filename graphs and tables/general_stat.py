import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# Функция для получения курса валют
def get_currency_rate(currency: str, date: str) -> float:
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)
    response.encoding = 'windows-1251'
    if response.status_code == 200:
        from xml.etree import ElementTree as ET
        tree = ET.fromstring(response.text)
        for valute in tree.findall(".//Valute"):
            char_code = valute.find("CharCode").text
            if char_code == currency:
                rate = float(valute.find("Value").text.replace(',', '.'))
                nominal = int(valute.find("Nominal").text)
                return rate / nominal
    return 1.0 if currency == "RUR" else None

# Загрузка данных
file_path = "vacancies_2024.csv"

vacancies = pd.read_csv(file_path, dtype={
    "name": str,
    "key_skills": str,
    "salary_from": float,
    "salary_to": float,
    "salary_currency": str,
    "area_name": str,
    "published_at": str
})

# Обработка пропусков
vacancies["key_skills"] = vacancies["key_skills"].fillna("")


# Предобработка данных
vacancies = vacancies[vacancies["salary_from"].notnull() | vacancies["salary_to"].notnull()]

# Исключение некорректных зарплат
vacancies = vacancies[(vacancies["salary_from"] <= 10_000_000) & (vacancies["salary_to"] <= 10_000_000)]

# Расчет средней зарплаты
vacancies["salary_avg"] = vacancies[["salary_from", "salary_to"]].mean(axis=1)

# Конвертация зарплат в рубли
converted_salaries = []
for _, row in vacancies.iterrows():
    date = datetime.strptime(row["published_at"].split("T")[0], "%Y-%m-%d").strftime("%d/%m/%Y")
    rate = get_currency_rate(row["salary_currency"], date)
    if rate:
        converted_salaries.append(row["salary_avg"] * rate)
    else:
        converted_salaries.append(None)

vacancies["salary_rub"] = converted_salaries

# Группировка по годам и расчет среднего уровня зарплат
vacancies["year"] = pd.to_datetime(vacancies["published_at"]).dt.year
salary_trend = vacancies.groupby("year")["salary_rub"].mean().dropna()

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(salary_trend.index, salary_trend.values, marker='o', label="Средняя зарплата")
plt.title("Динамика уровня зарплат по годам")
plt.xlabel("Год")
plt.ylabel("Средняя зарплата (в рублях)")
plt.grid(True)
plt.legend()

# Сохранение графика
plt.savefig("salary_trend.png")
plt.show()
