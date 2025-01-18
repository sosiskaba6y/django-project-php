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

# Группировка по городам и подсчет количества вакансий
vacancy_count_by_city = vacancies.groupby("area_name").size().reset_index(name='count')

# Общее количество вакансий
total_vacancies = len(vacancies)

# Рассчет доли вакансий по каждому городу
vacancy_count_by_city["proportion"] = vacancy_count_by_city["count"] / total_vacancies

# Сортировка по доле в порядке убывания
vacancy_count_by_city = vacancy_count_by_city.sort_values(by="proportion", ascending=False)

# Оставляем только топ N городов, остальные объединяем в "Другие"
top_n = 20  # Количество городов для отображения
top_cities = vacancy_count_by_city.head(top_n)
other_cities_proportion = vacancy_count_by_city["proportion"][top_n:].sum()
other_cities = pd.DataFrame({"area_name": ["Другие"], "count": [int(other_cities_proportion * total_vacancies)], "proportion": [other_cities_proportion]})

# Объединяем топ города и "Другие" города
final_data = pd.concat([top_cities, other_cities])

print(final_data)

# Построение графика
plt.figure(figsize=(12, 8))
plt.barh(final_data["area_name"], final_data["proportion"], color='skyblue')
plt.title(f"Доля вакансий по городам для всех профессий (в порядке убывания), ТОП-{top_n} + Другие", fontsize=14)
plt.xlabel("Доля вакансий", fontsize=12)
plt.ylabel("Город", fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("output/Доля вакансий по городам для всех профессий_top10_and_others.png")
plt.show()