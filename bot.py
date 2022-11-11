# from keys import bot, API_token, apiKey
from get_function.passwords import generate_random_password
from get_function.weather import get_current_weather
from get_function.reminder_func import get_reminder_days
from get_function.translate import get_your_translate
import telebot


bot =telebot.TeleBot('5141952410:AAGe2h9TmxyPrcajc5DliqbrBdSgiu4_ICA')
API_token = 'b3bac59fbc7c91b92084626e3e72ec66'
apiKey = '6QH0KNY-F9QMSFK-QG52CWT-EZ54JYS'


def get_weather_func(message):
    weather = get_current_weather(message.text, API_token)
    bot.send_message(message.chat.id, weather)


def get_translate_func(message):
    translate = get_your_translate(message.text, apiKey)
    bot.send_message(message.chat.id, translate)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    response_message = bot.reply_to(message,
                                    f'Hello, {message.from_user.first_name} {message.from_user.last_name}\n'
                                    f'If you need a password, type the command "/password"\n'
                                    f'If you need to know the current weather, type the command "/weather"\n'
                                    f'If you want to translate text from Ru into En, type the command "/translate"\n'
                                    f'If you want to see a reminder, type the command "/reminder"')

    bot.register_next_step_handler(response_message, get_choice)


@bot.message_handler(commands=['weather', 'password', 'translate', 'reminder'])
def get_choice(message):
    if message.text == '/weather':
        response_message = bot.reply_to(message, "Input name of the city:\n")
        bot.register_next_step_handler(response_message, get_weather_func)
    elif message.text == '/reminder':
        generation = get_reminder_days()
        bot.send_message(message.chat.id, generation)
    elif message.text == '/password':
        generation = generate_random_password()
        bot.send_message(message.chat.id, generation)
    elif message.text == '/translate':
        response_message = bot.reply_to(message, "Input some text:\n")
        bot.register_next_step_handler(response_message, get_translate_func)


bot.polling()
