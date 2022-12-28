import os
import telebot
import datetime
import re

from data.bot_data import BotDataProvide
from get_function.passwords import generate_random_password
from get_function.weather import get_current_weather
from get_function.translate import get_your_translate


bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
db = BotDataProvide("date_for_tg.db")


def get_weather_func(message):
    weather = get_current_weather(message.text, os.getenv('WEATHER_API_TOKEN'))
    bot.send_message(message.chat.id, weather)


def get_generated_password(message):
    generation = generate_random_password(message.text)
    bot.send_message(message.chat.id, generation)


def get_translate_func(message):
    translate = get_your_translate(message.text, os.getenv('TRANSLATOR_API_TOKEN'))
    bot.send_message(message.chat.id, translate)


def add_user_dates_in_db(message):
    if re.match(r'\d{2}/\d{2}/\d{4}-\w*\s?.*', message.text):
        user_date = message.text.split("-")[0]
        date_description = message.text.split("-", 1)[1]
        pars_user_day = user_date[0:2]
        pars_user_month = user_date[3:5]
        pars_user_year = user_date[6:10]
        if int(pars_user_day) <= 31 and int(pars_user_month) <= 12 and int(pars_user_year) <= 2050:
            db.set_user_date(message.chat.id, user_date, date_description)
            bot.send_message(message.chat.id, f'Your date was added')
        else:
            bot.send_message(message.chat.id,
                             f'Wrong entry, your day must be no more than 31, your month must be no more than 12 '
                             f'and your year must be no more than 2050, try again.')
    else:
        bot.send_message(message.chat.id,
                         f'Wrong input, You need input like "22/12/2023-very important day" and try again')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name} {message.from_user.last_name}\n'
                                      f'If you need a password, type the command "/password"\n'
                                      f'If you need to know the current weather, type the command "/weather"\n'
                                      f'If you want to add your dates, type the command "/add"\n'
                                      f'If you want to see all your dates type the command "/get"\n'
                                      f'If you want to see how many days are left until your dates, '
                                      f'type the command "/reminder"')


@bot.message_handler(commands=['weather'])
def send_weather(message):
    response_message = bot.reply_to(message, "Input name of the city:\n")
    bot.register_next_step_handler(response_message, get_weather_func)


@bot.message_handler(commands=['password'])
def send_generated_password(message):
    response_message = bot.reply_to(message, "Input the desired password length:\n")
    bot.register_next_step_handler(response_message, get_generated_password)


@bot.message_handler(commands=['translate'])
def send_translated_message(message):
    response_message = bot.reply_to(message, "Input some text:\n")
    bot.register_next_step_handler(response_message, get_translate_func)


@bot.message_handler(commands=['add'])
def add_reminder_dates_to_db(message):
    response_message = bot.reply_to(message, "Date and description (example '22/12/2023-very important day').\n")
    bot.register_next_step_handler(response_message, add_user_dates_in_db)


@bot.message_handler(commands=['get'])
def look_at_all_user_dates(message):
    dates = []
    dates_of_user = db.get_from(message.chat.id)
    for single_date in dates_of_user:
        date_and_description = single_date[2] + ' ' + single_date[3]
        dates.append(date_and_description)
    dates = '\n'.join(dates)
    bot.send_message(message.chat.id, f' That`s yours dates \n{dates}')


@bot.message_handler(commands=['reminder'])
def pic_up_the_counted_dates(message):
    dates = []
    dates_user = db.get_from(message.chat.id)
    if dates_user <= dates:
        bot.send_message(message.chat.id, f'Yours list empty, you need use command "/add" before')
    else:
        for single_date in dates_user:
            date = single_date[2]
            description = single_date[3]
            date_now = datetime.datetime.now()
            date_x = datetime.datetime.strptime(date, '%d/%m/%Y').replace(year=date_now.year)
            if date_x < date_now:
                date_x = date_x.replace(year=date_now.year + 1)
            days_until = date_x - date_now
            dates.append(f'{days_until.days} days until {description}.')
        dates_update = '\n'.join(dates)
        bot.send_message(message.chat.id, dates_update)


bot.polling()
