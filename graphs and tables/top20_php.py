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


# Функция для разбиения значений в столбце key_skills на отдельные навыки
def split_skills(skills):
    if pd.isna(skills):
        return []
    # Разделяем по запятой и переносу строки
    skills_list = [skill.strip() for skill in str(skills).replace('\n', ',').split(',') if skill.strip()]
    return skills_list


# Применение функции для разбиения навыков
php_vacancies["skills_list"] = php_vacancies["key_skills"].apply(split_skills)

# Взрыв списка навыков в отдельные строки
skills_df = php_vacancies.explode("skills_list")

# Группировка по году и навыку, подсчет количества упоминаний каждого навыка
skills_count_by_year = skills_df.groupby(["year", "skills_list"])["skills_list"].count().rename("count").reset_index()

# Нахождение ТОП-20 навыков для каждого года
top_skills_by_year = skills_count_by_year.groupby("year").apply(lambda x: x.nlargest(20, "count")).reset_index(
    drop=True)

# Создание HTML таблицы
html_table = "<table class='iksweb'>\n<tbody>\n"

years = sorted(top_skills_by_year["year"].unique())
for year in years:
    year_data = top_skills_by_year[top_skills_by_year["year"] == year]
    labels = year_data["skills_list"].tolist()
    sizes = year_data["count"].tolist()

    html_table += f"<tr><td rowspan='2'>{year}</td><td>Скилл</td>"
    html_table += "".join(f"<td>{label}</td>" for label in labels)
    html_table += "</tr>\n"

    html_table += "<tr><td>Количество</td>"
    html_table += "".join(f"<td>{size}</td>" for size in sizes)
    html_table += "</tr>\n"

html_table += "</tbody></table>"

# Сохранение HTML таблицы в файл
with open("output/top_skills_html_table.html", "w", encoding="utf-8") as file:
    file.write(html_table)

print("HTML таблица создана и сохранена в файл output/top_skills_html_table.html")

# Определение количества строк и столбцов для подграфиков
n_years = len(years)
n_cols = 3  # Количество графиков в одном ряду
n_rows = (n_years + n_cols - 1) // n_cols  # Округляем вверх до ближайшего целого числа

# Создаем общую фигуру и оси для всех круговых диаграмм
fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 6 * n_rows))
axes = axes.flatten()  # Преобразуем массив осей в одномерный массив

# Строим круговую диаграмму для каждого года
for i, year in enumerate(years):
    year_data = top_skills_by_year[top_skills_by_year["year"] == year]
    labels = year_data["skills_list"]
    sizes = year_data["count"]

    ax = axes[i]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
    ax.set_title(f"ТОП-20 навыков за {year} год")

# Скрываем лишние оси
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.savefig("output/ТОП-20 навыков по годам.png")
plt.show()

print("Круговые диаграммы созданы и сохранены в файл output/ТОП-20 навыков по годам.png")