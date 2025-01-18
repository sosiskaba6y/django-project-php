import pandas as pd

# Чтение CSV файла
df = pd.read_csv('vacancies_2024.csv', low_memory=False)

# Преобразование столбца 'published_at' в формат datetime
df['published_at'] = pd.to_datetime(df['published_at'])

# Получение минимальной и максимальной даты публикации
min_date = df['published_at'].min()
max_date = df['published_at'].max()

print(f"Минимальная дата публикации: {min_date}")
print(f"Максимальная дата публикации: {max_date}")

# Получение списка всех валют без повторений
unique_currencies = df['salary_currency'].dropna().unique()

print("Список всех валют без повторений:")
print(unique_currencies)