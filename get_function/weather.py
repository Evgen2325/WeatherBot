import requests
import datetime
from loguru import logger


def get_current_weather(city, api_token):
    code_smile = {'Clear': 'Ясно\U00002600',
                  'Clouds': 'Облачно\U00002601',
                  'Thunderstorm': 'Гроза\U000026A1',
                  'Rain': 'Дождь\U00002614',
                  'Drizzle': 'Дождь\U00002614',
                  'Snow': 'Снег\U0001F328',
                  'Mist': 'Туман\U0001F32B', }
    try:
        logger.info(f'User use the function get_current_weather')
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
