import telebot
import requests
import datetime
import random
import json
import csv

bot = telebot.TeleBot("5141952410:AAGe2h9TmxyPrcajc5DliqbrBdSgiu4_ICA")
API_token = 'b3bac59fbc7c91b92084626e3e72ec66'
apiKey = '6QH0KNY-F9QMSFK-QG52CWT-EZ54JYS'


def get_weather(city, api_token):
    code_smile = {'Clear': 'Ясно\U00002600',
                  'Clouds': 'Облачно\U00002601',
                  'Thunderstorm': 'Гроза\U000026A1',
                  'Rain': 'Дождь\U00002614',
                  'Drizzle': 'Дождь\U00002614',
                  'Snow': 'Снег\U0001F328',
                  'Mist': 'Туман\U0001F32B', }
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_token}&lang=ru&units=metric')
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


def get_weather_func(message):
    weather = get_weather(message.text, API_token)
    bot.send_message(message.chat.id, weather)


def get_reminder():
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
        return '\n'.join(list_result)


def generation_password():
    symbols = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM.,\?!-_'
    length = random.randint(10, 20)
    password = ''
    for i in range(int(length)):
        password += random.choice(symbols)
    return password


def get_translate(user_input, api_key):
    headers = {
        'X-API-Key': api_key,
        'Content-Type': 'text/xml; charset=utf-8; application/json',
        'Accept': 'application/json',
    }
    data = '{"texts": ["' + user_input + '"]  ,\n'  '"to": ["en"],\n        "from": "ru"\n    }'
    response = requests.post('https://api.lecto.ai/v1/translate/text', headers=headers, data=data.encode('utf-8'))
    var_json_object = json.loads(response.text)

    translation = var_json_object.get('translations')[0].get('translated')[0]
    return f'Твой перевод:\n\n{translation}'


def get_translate_func(message):
    translate = get_translate(message.text, apiKey)
    bot.send_message(message.chat.id, translate)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    response_message = bot.reply_to(message,
                                    f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n'
                                    f'Eсли нужен пароль, введи слово "/password"\n'
                                    f'Если хочешь узнать прогноз погоды, введи слово "/weather"\n'
                                    f'Если хочешь перевести текст с русского на английский , введи слово "/translate"\n'
                                    f'Если хочешь вызвать напоминание, введи команду "/reminder"')

    bot.register_next_step_handler(response_message, get_choice)


@bot.message_handler(commands=['weather', 'password', 'translate', '/reminder'])
def get_choice(message):
    if message.text == '/weather':
        response_message = bot.reply_to(message, "Введите название города:\n")
        bot.register_next_step_handler(response_message, get_weather_func)
    elif message.text == '/reminder':
        generation = get_reminder()
        bot.send_message(message.chat.id, generation)
    elif message.text == '/password':
        generation = generation_password()
        bot.send_message(message.chat.id, generation)
    elif message.text == '/translate':
        response_message = bot.reply_to(message, "Введите текст:\n")
        bot.register_next_step_handler(response_message, get_translate_func)


bot.polling()
