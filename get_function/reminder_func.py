import datetime
import csv



def get_reminder_days():
    result_dates = []
    with open('file.csv', 'r') as f:
        reader = csv.reader(f)
        date_now = datetime.datetime.now()
        for line in reader:
            parsed_date = line[0]
            description = line[1]
            date_x = datetime.datetime.strptime(parsed_date, '%d/%m/%Y').replace(year=date_now.year)
            if date_x < date_now:
                date_x = date_x.replace(year=date_now.year + 1)
            days_until = date_x - date_now
            result_dates.append(f'{days_until.days} days until {description}.')
        return '\n'.join(result_dates)