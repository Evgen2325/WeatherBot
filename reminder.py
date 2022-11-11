import csv
import datetime

with open('file.csv', 'r') as f:
    list_result = []
    reader = csv.reader(f)
    date_now = datetime.datetime.now().replace(microsecond=0)
    for line in reader:
        date_born = line[0]
        date_born = datetime.datetime.strptime(date_born, '%d.%m.%Y')
        date_born = date_born.replace(year=date_now.year)
        if date_now > date_born:
            date_born = date_born.replace(year=date_now.year + 1)
            data_x = date_born - date_now
        elif date_now < date_born:
            date_born = date_born.replace(year=date_now.year)
            data_x = date_born - date_now
        list_result.append(f'До {line[1]} осталось {data_x.days} дней')
    print('\n'.join(list_result))





