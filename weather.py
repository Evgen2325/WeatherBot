# import telebot
import requests
import datetime

#bot = telebot.TeleBot("5141952410:AAGe2h9TmxyPrcajc5DliqbrBdSgiu4_ICA")
weather_tokin = '4b73a57dc251d33c9042835b2d1dc0ec'

def get_weather(city, weather_tokin ):

    code_smile = {'Clear': 'Ясно\U00002600',
                  'Clouds': 'Облачно\U00002601',
                  'Thunderstorm': 'Гроза\U000026A1',
                  'Rain': 'Дождь\U00002614',
                  'Drizzle': 'Дождь\U00002614',
                  'Snow': 'Снег\U0001F328',
                  'Mist': 'Туман\U0001F32B',}
    try:
        url_ = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_tokin}&lang=ru&units=metric')
        data = url_.json()


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

        print(f'--------{datetime.datetime.now().strftime("%c")}--------\n'
              f'Погода в городе: {city}\nТемпература: {cur_weather}C°{wd}\n'
              f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n'
              f'Ветер: {wind}м/с')

    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def main():
    city = input()
    get_weather(city, weather_tokin)

if __name__ == '__main__':
     main()





#bot.polling()