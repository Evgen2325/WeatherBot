import telebot
import requests
import datetime
import random
import json

bot = telebot.TeleBot("5141952410:AAGe2h9TmxyPrcajc5DliqbrBdSgiu4_ICA")
API_tokin = 'b3bac59fbc7c91b92084626e3e72ec66'
apiKey = '6QH0KNY-F9QMSFK-QG52CWT-EZ54JYS'

def get_weather(city, API_tokin):
    code_smile = {'Clear': 'Ясно\U00002600',
                  'Clouds': 'Облачно\U00002601',
                  'Thunderstorm': 'Гроза\U000026A1',
                  'Rain': 'Дождь\U00002614',
                  'Drizzle': 'Дождь\U00002614',
                  'Snow': 'Снег\U0001F328',
                  'Mist': 'Туман\U0001F32B', }
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_tokin}&lang=ru&units=metric')
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

def get_translate(user_input, apiKey):
    headers = {
        'X-API-Key': apiKey,
        'Content-Type': 'text/xml; charset=utf-8; application/json',
        'Accept': 'application/json',
    }
    user_input = input("Введите текс ")
    data = '{"texts": ["' + user_input + '"]  ,\n'  '"to": ["en"],\n        "from": "ru"\n    }'
    response = requests.post('https://api.lecto.ai/v1/translate/text', headers=headers, data=data.encode('utf-8'))
    var_json_object = json.loads(response.text)

    translation = var_json_object.get('translations')[0].get('translated')[0]
    return f'Твой перевод:\n\n{translation}'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = bot.reply_to(message, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n'
                                 f'Eсли нужен пароль, введи слово "/password"\n'
                                 f'Если хочешь узнать прогноз погоды, введи слово "/weather"\n'
                                 f'Если хочешь перевести текст с русского на английский , введи слово "/translate"')
    bot.register_next_step_handler(name, get_choice)
@bot.message_handler(commands=['weather', 'password', 'translate'])
def get_choice(message):
    if message.text == '/weather':
        weather = get_weather(message.text, API_tokin)
        bot.send_message(message.chat.id, weather)
    elif message.text == '/password':
        generation = generation_password()
        bot.send_message(message.chat.id, generation)
    elif message.text == '/translate':
        translate = get_translate(message.text, apiKey)
        bot.send_message(message.chat.id, translate)




        # name = bot.reply_to(message, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n'
        #                              f'Eсли нужен пароль, введи слово "/password"\n'
        #                              f'Если хочешь узнать прогноз погоды, введи слово "/weather"\n'
        #                              f'Если хочешь перевести текст с русского на английский , введи слово "/translate"')
        # bot.register_next_step_handler(name, send_weather)


# def send_weather(message):
#     if message.text == '/weather':
#        weather = get_weather(message.text, API_tokin)
#        bot.send_message(message.chat.id, weather)
    #elif message.text != '/weather':
        # name = bot.reply_to(message, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n'
        #                          f'Eсли нужен пароль, введи слово "/password"\n'
        #                          f'Если хочешь узнать прогноз погоды, введи слово "/weather"\n'
        #                          f'Если хочешь перевести текст с русского на английский , введи слово "/translate"')
         #bot.register_next_step_handler(message.chat.id, send_translate)

# def send_translate(message):
#      if message.text == '/translate':
#          translate = get_translate()
#          bot.send_message(message.chat.id, translate)
     #elif message.text != '/translate':
     #    name = bot.reply_to(message, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n'
     #                             f'Eсли нужен пароль, введи слово "/password"\n'
     #                             f'Если хочешь узнать прогноз погоды, введи слово "/weather"\n'
     #                             f'Если хочешь перевести текст с русского на английский , введи слово "/translate"')
         #bot.register_next_step_handler(message.chat.id, send_welcome)





# @bot.message_handler(commands=['/translate'])
# def send_translate(message):
#     if message.text == '/translate':
#         translate = get_translate()
#         bot.send_message(message.chat.id, translate)

# @bot.message_handler(content_types=['text'])
# def send_weather(message):
#     if message.text == '/weather':
#         weather = get_weather(message.text, API_tokin)
#         bot.send_message(message.chat.id, weather)
#
# @bot.message_handler(content_types=['text'])
# def send_translate(message):
#     if message.text == '/translate':
#         translate = get_translate()
#         bot.send_message(message.chat.id, translate)



bot.polling()
