import pandas as pd

# Путь к файлу с вакансиями
vacancies_file = "vacancies_2024.csv"

# Загрузка данных
vacancies = pd.read_csv(vacancies_file)

# Удаление строк с некорректной датой (если необходимо)
# Здесь мы не удаляем строки с пустыми значениями, так как нужно учитывать все вакансии
# vacancies = vacancies.dropna(subset=["published_at"])

# Группировка по городам и подсчет количества вакансий
vacancy_count_by_city = vacancies.groupby("area_name").size().reset_index(name='count')

# Общее количество вакансий
total_vacancies = len(vacancies)

# Рассчет доли вакансий по каждому городу
vacancy_count_by_city["proportion"] = vacancy_count_by_city["count"] / total_vacancies

# Сортировка по доле в порядке убывания
vacancy_count_by_city = vacancy_count_by_city.sort_values(by="proportion", ascending=False)

print(vacancy_count_by_city)

# Построение графика
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.bar(vacancy_count_by_city["area_name"], vacancy_count_by_city["proportion"], color='skyblue')
plt.title("Доля вакансий по городам (в порядке убывания)", fontsize=14)
plt.xlabel("Город", fontsize=12)
plt.ylabel("Доля вакансий", fontsize=12)
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("output/Доля вакансий по городам.png")
plt.show()