import os
import telebot

from data.bot_data import BotDataProvide
from get_function.passwords import generate_random_password
from get_function.weather import get_current_weather
from get_function.reminder_func import get_reminder_days
from get_function.translate import get_your_translate

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
db = BotDataProvide("date_for_tg.db")


def get_weather_func(message):
    weather = get_current_weather(message.text, os.getenv('WEATHER_API_TOKEN'))
    bot.send_message(message.chat.id, weather)


def get_translate_func(message):
    translate = get_your_translate(message.text, os.getenv('TRANSLATOR_API_TOKEN'))
    bot.send_message(message.chat.id, translate)


def get_date_from_user_to_update_db(message):
    # TODO add assertion for string
    print(message.text)
    print(message.chat.id)
    user_date = message.text.split("-")[0]
    date_description = message.text.split("-")[1]
    print(db.set_user_date(message.chat.id, user_date, date_description))
    # bot.send_message(message.chat.id, f"wrong input, you need input like (example '22/12/2023-mothers day')\n")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    response_message = bot.reply_to(message,
                                    f'Hello, {message.from_user.first_name} {message.from_user.last_name}\n'
                                    f'If you need a password, type the command "/password"\n'
                                    f'If you need to know the current weather, type the command "/weather"\n'
                                    f'If you want to translate text from Ru into En, type the command "/translate"\n'
                                    f'If you want to see a reminder, type the command "/reminder"')
    bot.send_message(message.chat.id, response_message)


@bot.message_handler(commands=['weather'])
def send_weather(message):
    response_message = bot.reply_to(message, "Input name of the city:\n")
    bot.register_next_step_handler(response_message, get_weather_func)


@bot.message_handler(commands=['password'])
def send_generated_password(message):
    generation = generate_random_password()
    bot.send_message(message.chat.id, generation)


@bot.message_handler(commands=['translate'])
def send_translated_message(message):
    response_message = bot.reply_to(message, "Input some text:\n")
    bot.register_next_step_handler(response_message, get_translate_func)


@bot.message_handler(commands=['reminder'])
def send_reminder_dates_from_csv(message):
    generation = get_reminder_days()
    bot.send_message(message.chat.id, generation)


@bot.message_handler(commands=['add'])
def add_reminder_dates_to_db(message):
    response_message = bot.reply_to(message, "Date and desription (example '22/12/2023-mothers day')\n")
    bot.register_next_step_handler(response_message, get_date_from_user_to_update_db)


@bot.message_handler(commands=['get'])
def get_reminder_dates_from_db(message):
    dates = []
    descriptions = []
    dates_for_user = db.get_from(message.chat.id)
    for single_date in dates_for_user:
        date = single_date[2]
        description = single_date[3]
        dates.append(date)
        descriptions.append(description)
    print(descriptions)
    print(dates)
    # bot.send_message(message.chat.id, result_string)


bot.polling()
