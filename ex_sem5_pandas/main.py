import pandas as pd
import numpy as np
from functions import *

data = pd.read_excel('data.xlsx')
data['Фамилия'] = data['ФИО сотрудника'].str.split().str[0]
data['Имя'] = data['ФИО сотрудника'].str.split().str[1]
data['Отчество'] = data['ФИО сотрудника'].str.split().str[2]
data["проверка"] = pd.isnull(data['Дата увольнения'])

data['Пол'] = data['Отчество'].apply(determine_gender)
data['Возраст на дату приема'] = (data['Дата приема'] - data['Дата рождения']).dt.days // 365
data['Пенсионный возраст'] = np.where(data['Возраст на дату приема'] >= 60, 'да', 'нет')
data['Стаж'] = ((data['Дата увольнения'].replace({pd.NaT: '01-01-2017'}) - data['Дата приема']).dt.days).apply(format_experience)

working_on_2017 = len(data[(data['Дата приема'] <= '2017-01-01') & ((data['Дата увольнения'].isnull()) | (data['Дата увольнения'] > '2017-01-01'))])
dismissed_by_2017 = len(data[(data['Дата увольнения'].notnull()) & (data['Дата увольнения'] <= '2017-01-01')])
dismissed_by_2009 = len(data[(data['Дата увольнения'].notnull()) & (data['Дата увольнения'] <= '2009-01-01')])

#создает датафрейм, в котором хранятся только уволенные сотрудники
dismissed_employees = data[data['Дата увольнения'].notnull()]

#находит средний возраст уволенных сотрудников
average_age_dismissed = ((dismissed_employees['Дата увольнения'] - dismissed_employees['Дата рождения']).dt.days // 365).mean()

#находит количество уволенных сотрудников по полу
dismissals_by_gender = dismissed_employees['Пол'].value_counts()

#находит количество сотрудников, фамилия которых начинается на 'М'
employees_with_last_name_M = len(data[data['Фамилия'].str.startswith('М', na=False)])

#удаляет все строки, в которых значение в столбце 'Причина увольнения' равно NaN, затем находит количество уникальных значений
unique_dismissal_reasons = len(data['Причина увольнения'].dropna().unique())

#находит моду (наиболее часто встречающееся значение) в столбце 'Причина увольнения'
most_common_dismissal_reason = data['Причина увольнения'].mode().values[0]




print(f"Количество сотрудников, работавших на 01.01.2017: {working_on_2017}")
print(f"Количество уволенных сотрудников до 01.01.2017: {dismissed_by_2017}")
print(f"Количество уволенных сотрудников до 01.01.2009: {dismissed_by_2009}")
print(f"Средний возраст уволенных: {average_age_dismissed:.2f}")
if dismissals_by_gender['женский'] > dismissals_by_gender['мужской']:
    print("Больше уволено женщин")
elif dismissals_by_gender['женский'] < dismissals_by_gender['мужской']:
    print("Больше уволено мужчин")
else:
    print("Уволено одинаковое количество женщин и мужчин")
print(f"Количество сотрудников с фамилией на букву 'М': {employees_with_last_name_M}")
print(f"Количество уникальных причин увольнения: {unique_dismissal_reasons}")
print(f"Самая частая причина увольнения: {most_common_dismissal_reason}")
