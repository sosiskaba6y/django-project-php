import pandas as pd
import requests
from lxml import etree
from datetime import datetime

CURRENCIES = ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS', 'GEL']

start_date = '2003-01-01'
end_date = '2024-12-03'
date = datetime.strptime(start_date, '%Y-%m-%d')
end = datetime.strptime(end_date, '%Y-%m-%d')
data = []
while date <= end:
    date_str = date.strftime('%d/%m/%Y')
    response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}')
    tree = etree.fromstring(response.content)
    year_month = date.strftime('%Y-%m')
    row = [year_month]
    for currency in CURRENCIES:
        element = tree.xpath(f"//Valute[CharCode='{currency}']")
        value = (float(element[0].find('Value').text.replace(',', '.')) / int(
            element[0].find('Nominal').text)) if element else None
        row.append(round(value, 8) if value else None)
    data.append(row)
    if date.month == 12:
        date = date.replace(year=date.year + 1, month=1)
    else:
        date = date.replace(month=date.month + 1)
df = pd.DataFrame(data, columns=['date'] + CURRENCIES)
df.to_csv('currency.csv', index=False)

