import os

import telebot
from telebot import types

from dotenv import load_dotenv

from api_handlers.dadata_api_handler import DadataAPIHandler
from api_handlers.weather_api_handler import WeatherAPIHandler

load_dotenv()
TG_TOKEN: str = os.environ.get("TG_TOKEN")

bot = telebot.TeleBot(TG_TOKEN)
user_shared_location = []

#вывод приветствия и создание кнопок
@bot.message_handler(commands=["start"])
@bot.message_handler(
    func=lambda message: message.text == '◀️Назад',
    content_types=['text']
)
def ask_for_location(message):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Введите название города"
    )
    share_location_button = types.KeyboardButton(
        text="📍Поделиться местоположением",
        request_location=True
    )
    request_forecast_button = types.KeyboardButton(
        text="⏰Прогноз"
    )
    keyboard.add(share_location_button, request_forecast_button)
    bot.send_message(
        message.from_user.id,
        "Отправьте свое местоположение или введите название города",
        reply_markup=keyboard
    )

# обработка нажатия на кнопку "Прогноз", вывод преложений по сроку прогноза
@bot.message_handler(
    func=lambda message: message.text == '⏰Прогноз',
    content_types=['text']
)
def suggest_forecast_duration(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    request_3h_forecast_button = types.KeyboardButton(text="🕒3 часа")
    request_6h_forecast_button = types.KeyboardButton(text="🕕6 часов")
    request_12h_forecast_button = types.KeyboardButton(text="🕛12 часов")
    request_tomorrow_forecast_button = types.KeyboardButton(text="🕐Завтра")
    request_after_tomorrow_forecast_button = types.KeyboardButton(text="🕐Послезавтра")
    back_button = types.KeyboardButton(text="◀️Назад")

    keyboard.add(
        request_3h_forecast_button,
        request_6h_forecast_button,
        request_12h_forecast_button,
        request_tomorrow_forecast_button,
        request_after_tomorrow_forecast_button,
        back_button
    )
    bot.send_message(
        message.from_user.id,
        "Выберите срок прогноза",
        reply_markup=keyboard
    )

# обработка нажатия на кнопку "📍Поделиться местоположением"
@bot.message_handler(content_types=['location'])
def send_current_weather_by_coords(message):
        lat: float = message.location.latitude
        lon: float = message.location.longitude

        weather_api_handler = WeatherAPIHandler(lat, lon)
        weather_data = weather_api_handler.get_current_weather()

        city_data_api_handler = DadataAPIHandler(lat=lat, lon=lon)
        city_data = city_data_api_handler.get_city_data_by_coords()

        temperature: int = int(round(weather_data["main"]["temp"], 0))
        feels_like: int = int(round(weather_data["main"]["feels_like"], 0))
        weather_condition = weather_data["weather"][0]["description"]
        weather_condition_icon = weather_api_handler.get_weather_icon()

        city_type = city_data[0]["data"]["region_type"]
        city_name = city_data[0]["data"]["region"]

        reply = f"Погода в {city_type}.{city_name} сейчас:\n"\
                f"{weather_condition_icon}{weather_condition.capitalize()}\n"\
                f"<b>Температура: </b>{temperature}°C\n" \
                f"<b>Ощущается как: </b>{feels_like}°C"

        return bot.send_message(message.from_user.id, reply, parse_mode="html")


# обработка отправки пользователем названия города вручную
@bot.message_handler(
    func=lambda message: message.text not in ['⏰Прогноз', '◀️Назад'],
    content_types=['text']
)
def send_current_weather_by_city(message):
        city = message.text.capitalize()
        city_data_api_handler = DadataAPIHandler(city=city)
        city_coords = city_data_api_handler.get_coords_by_city()
        if city_coords["result"] is None:
            return bot.send_message(message.from_user.id, "Такой город не найден")
        else:
            lat = city_coords["geo_lat"]
            lon = city_coords["geo_lon"]
            city_type = city_coords["region_type"]
            city_name = city_coords["region"]

            weather_api_handler = WeatherAPIHandler(lat, lon)
            weather_data = weather_api_handler.get_current_weather()
            temperature: int = int(round(weather_data["main"]["temp"], 0))
            feels_like: int = int(round(weather_data["main"]["feels_like"], 0))
            weather_condition = weather_data["weather"][0]["description"]
            weather_condition_icon = weather_api_handler.get_weather_icon()

            reply = f"Погода в {city_type}.{city_name} сейчас:\n" \
                    f"{weather_condition_icon}{weather_condition.capitalize()}\n" \
                    f"<b>Температура: </b>{temperature}°C\n" \
                    f"<b>Ощущается как: </b>{feels_like}°C"

        return bot.send_message(message.from_user.id, reply, parse_mode="html")





if __name__ == "__main__":
    bot.infinity_polling()
