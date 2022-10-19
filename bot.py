import telebot
import requests
import datetime
import random

bot = telebot.TeleBot("5141952410:AAGe2h9TmxyPrcajc5DliqbrBdSgiu4_ICA")
API_tokin = '4b73a57dc251d33c9042835b2d1dc0ec'


def get_weather(city, api_tokin):
    code_smile = {'Clear': 'Ясно\U00002600',
                  'Clouds': 'Облачно\U00002601',
                  'Thunderstorm': 'Гроза\U000026A1',
                  'Rain': 'Дождь\U00002614',
                  'Drizzle': 'Дождь\U00002614',
                  'Snow': 'Снег\U0001F328',
                  'Mist': 'Туман\U0001F32B', }
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_tokin}&lang=ru&units=metric')
        data = response.json()

        city = data['name']
        cur_weather = data['main']['temp']
        weather_description = data['weather'][0]['main']
        if weather_description in code_smile:
            wd = code_smile[weather_description]
        else:
            wd = 'Посмотри в окно и сам идентифицируй!!!'
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']

        return (f'--------{datetime.datetime.now().strftime("%c")}--------\n'
                f'Погода в городе: {city}\nТемпература: {cur_weather}C°{wd}\n'
                f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n'
                f'Ветер: {wind}м/с')

    except Exception:
        return 'Введите название города'


def generation_password():
    symbols = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM.,\?!-_'
    lenght = random.randint(10, 20)
    password = ''
    for i in range(int(lenght)):
        password += random.choice(symbols)
    return password


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = (f'Привет, {message.from_user.first_name} {message.from_user.last_name} , если нужен пароль, введи слово "/password"\n'
            f'Если хочешь узнать прогноз погоды, введи слово "/weather"')
    bot.send_message(message.chat.id, name)


@bot.message_handler(content_types=['text'])
def send_password_weather(message):
    if message.text == '/password':
        generation = generation_password()
        bot.send_message(message.chat.id, generation)
    elif message.text != '/password':
        weather = get_weather(message.text, API_tokin)
        bot.send_message(message.chat.id, weather)


bot.polling()
