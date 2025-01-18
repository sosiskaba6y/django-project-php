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


# Функция для разбиения значений в столбце key_skills на отдельные навыки
def split_skills(skills):
    if pd.isna(skills):
        return []
    # Разделяем по запятой и переносу строки
    skills_list = [skill.strip() for skill in str(skills).replace('\n', ',').split(',') if skill.strip()]
    return skills_list


# Применение функции для разбиения навыков
vacancies["skills_list"] = vacancies["key_skills"].apply(split_skills)

# Взрыв списка навыков в отдельные строки
skills_df = vacancies.explode("skills_list")

# Группировка по году и навыку, подсчет количества упоминаний каждого навыка
skills_count_by_year = skills_df.groupby(["year", "skills_list"])["skills_list"].count().rename("count").reset_index()

# Нахождение ТОП-20 навыков для каждого года
top_skills_by_year = skills_count_by_year.groupby("year").apply(lambda x: x.nlargest(20, "count")).reset_index(
    drop=True)

# Получаем список уникальных лет
years = sorted(top_skills_by_year["year"].unique())

# Определяем количество строк и столбцов для подграфиков
n_years = len(years)
n_cols = 3  # Количество графиков в одном ряду
n_rows = (n_years + n_cols - 1) // n_cols  # Округляем вверх до ближайшего целого числа

# Создаем общую фигуру и оси для всех круговых диаграмм
fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 6 * n_rows))
axes = axes.flatten()  # Преобразуем массив осей в одномерный массив

# Строим круговую диаграмму и выводим таблицу для каждого года
for i, year in enumerate(years):
    year_data = top_skills_by_year[top_skills_by_year["year"] == year]

    if not year_data.empty:
        labels = year_data["skills_list"]
        sizes = year_data["count"]

        ax = axes[i]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
        ax.set_title(f"ТОП-20 навыков за {year} год")

        # Вывод таблицы для текущего года
        print(f"\nТОП-20 навыков за {year} год:")
        print(year_data[["skills_list", "count"]].to_string(index=False))

        # Сохранение круговой диаграммы для текущего года
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
        plt.title(f"ТОП-20 навыков за {year} год")
        plt.savefig(f"output/ТОП-20 навыков за {year} год.png")
        plt.close()
    else:
        # Если за этот год нет данных, просто скрываем ось
        axes[i].axis('off')

# Скрываем лишние оси
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.savefig("output/ТОП-20 навыков по годам.png")
plt.show()

# Вывод уникальных значений столбца year для проверки
print("\nУникальные годы в данных:")
print(sorted(vacancies["year"].unique()))