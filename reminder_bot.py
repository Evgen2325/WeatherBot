import telebot
import sqlite3
import datetime
import csv

# from first_sql_with_class import TelegrammBot
# from get_function.reminder_func import get_reminder_days

bot = telebot.TeleBot('5643692181:AAEvd665ZvwANdX1vcuf-T4eZVvk7CDBw3Y')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    response_message = f'Hello, {message.from_user.first_name} {message.from_user.last_name}\n'
    bot.send_message(message.chat.id, response_message)


@bot.message_handler(commands=['list'])
def add_table_db(message):
    connection = sqlite3.connect('date_for_tg.db')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'reminder' (ID INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, user_date DATE)")
    response_message = bot.reply_to(message, f'Список для добавления важных дат создан, введите дату')
    bot.register_next_step_handler(response_message, add_msg_user_to_db)
    connection.commit()


def add_msg_user_to_db(message):
    response_message = bot.reply_to(message, "your date is add\n")
    bot.register_next_step_handler(response_message, get_msg_user_from_db)
    connection = sqlite3.connect('date_for_tg.db')
    cursor = connection.cursor()
    # text = message.text
    user_data = message.text
    user_id = message.chat.id
    cursor.execute("INSERT INTO reminder (user_id, user_date) VALUES (?, ?)", (user_id, user_data))
    connection.commit()
    print(cursor.rowcount, "record inserted.")


@bot.message_handler(commands=['get'])
def get_msg_user_from_db(message):
    connection = sqlite3.connect('date_for_tg.db')
    cursor = connection.cursor()
    cursor.execute("SELECT user_date FROM reminder")
    sql = cursor.fetchall()
    for x in sql:
        print(x)
    bot.send_message(message.chat.id, x)
    connection.commit()


@bot.message_handler(commands=['reminder'])
def get_reminder_days(message):
    result_dates = []
    with open('date_for_tg.db', 'r') as f:
        reader = csv.reader(f)
        print(reader)
        date_now = datetime.datetime.now()
        print(date_now)
        for line in reader:
            parsed_date = line[0]
            description = line[1]
            date_x = datetime.datetime.strptime(parsed_date, '%d/%m/%Y').replace(year=date_now.year)
            if date_x < date_now:
                date_x = date_x.replace(year=date_now.year + 1)
            days_until = date_x - date_now
            result_dates.append(f'{days_until.days} days until {description}.')
        return '\n'.join(result_dates)






# @bot.message_handler(commands=['delete'])
# def del_msg_user_to_db(message):
#     pass


bot.polling()
