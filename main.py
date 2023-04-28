from config import TG_TOKEN
from parser import get_weather

import telebot

bot = telebot.TeleBot(TG_TOKEN, parse_mode='html')


@bot.message_handler(commands=['start'])
def welcome_message(message):
    weather_data = get_weather()

    temperature = weather_data["fact"]["temp"]
    feels_like = weather_data["fact"]["feels_like"]

    bot.send_message(message.chat.id, f"Привет,\nПогода в Москве:\n"
                                      f"<b>Температура:</b> {temperature}°C\n"
                                      f"<b>Ощущается как: </b>{feels_like}°C")


if __name__ == "__main__":
    bot.polling(none_stop=True)
