import os

import telebot
from telebot import types

from dotenv import load_dotenv

from handlers.dadata_api_handler import DadataAPIHandler
from handlers.file_handler import FileHandler
from handlers.weather_api_handler import WeatherAPIHandler

load_dotenv()
TG_TOKEN: str = os.environ.get("TG_TOKEN")

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=["start"])
@bot.message_handler(
    func=lambda message: message.text == '◀️Назад',
    content_types=['text']
)
def ask_for_location(message: object) -> None:
    """
    Выводит сообщение в чат
    и создает кнопку расшаривания местоположения пользователя.
    После чего сохраняет данные в json:
    id пользователя, широту, долготу, тип города, название города
    :param message: объект Message telegram API
    :type message: object
    """
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder="Введите название города"
    )
    share_location_button = types.KeyboardButton(
        text="📍Поделиться местоположением",
        request_location=True
    )
    keyboard.add(share_location_button)
    bot.send_message(
        message.from_user.id,
        "Отправьте свое местоположение или введите название города",
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['location'])
@bot.message_handler(
    func=lambda message: message.text == '◀️Назад',
    content_types=['text']
)
def process_location(message: object) -> None:
    """
    Получение геолокации от пользователя,
    сохранение данных в JSON.
    Отображение кнопок типа прогноза
    :param message: объект Message telegram API
    :type message: object
    """
    # сохранение данных локации в файл
    user_id = message.from_user.id
    lat: float = message.location.latitude
    lon: float = message.location.longitude

    city_data_api_handler = DadataAPIHandler(lat=lat, lon=lon)
    city_data = city_data_api_handler.get_city_data_by_coords()
    city_type = city_data[0]["data"]["region_type"]
    city_name = city_data[0]["data"]["region"]

    filehandler = FileHandler()
    if os.path.exists("chat_data.json") is False or os.stat("chat_data.json").st_size == 0:
        filehandler.save_chat_data_to_json(user_id, lat, lon, city_type, city_name)
    else:
        filehandler.update_chat_data_in_json(user_id, lat, lon, city_type, city_name)

    # конструктор кнопок
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    requests_for_current_weather_button = types.KeyboardButton(
        text="☀️Погода сейчас"
    )
    request_forecast_button = types.KeyboardButton(
        text="⏰Прогноз"
    )
    back_button = types.KeyboardButton(
        text='◀️Назад'
    )

    keyboard.add(
        requests_for_current_weather_button,
        request_forecast_button
    )
    keyboard.add(back_button)

    bot.send_message(
        message.from_user.id,
        "Выберите тип прогноза",
        reply_markup=keyboard
    )


# обработка отправки пользователем названия города вручную
@bot.message_handler(
    func=lambda message: message.text == "☀️Погода сейчас",
    content_types=['text']
)
def send_current_weather_by_coords(message: object) -> None:
    """
    Отправляет текущую погоду по координатам пользователя
    :param message: объект Message telegram API
    :type message: object
    """
    filehandler = FileHandler()
    data = filehandler.load_data_from_json()
    if message.from_user.id == data[0]['user_id']:
        lat = data[0]['lat']
        lon = data[0]['lon']
        city_type = data[0]['city_type']
        city_name = data[0]['city_name']

        weather_api_handler = WeatherAPIHandler(lat, lon)
        weather_data = weather_api_handler.get_current_weather()
        temperature: int = int(
            round(
                weather_data["main"]["temp"], 0
            )
        )
        feels_like: int = int(
            round(
                weather_data["main"]["feels_like"], 0
            )
        )
        weather_condition = weather_data["weather"][0]["description"]
        weather_condition_icon = weather_api_handler.get_weather_icon()

        reply = f"Погода в {city_type}.{city_name} сейчас:\n" \
                f"{weather_condition_icon}{weather_condition.capitalize()}\n" \
                f"<b>Температура: </b>{temperature}°C\n" \
                f"<b>Ощущается как: </b>{feels_like}°C"

        bot.send_message(message.from_user.id, reply, parse_mode="html")


# обработка нажатия на кнопку "Прогноз", вывод преложений по сроку прогноза
@bot.message_handler(
    func=lambda message: message.text == '⏰Прогноз',
    content_types=['text']
)
def suggest_forecast_duration(message: object) -> None:
    """
    Создает клавиатуру с вариантами срока прогноза
    :param message: объект Message telegram API
    :type message: object
    """
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
    )
    keyboard.add(back_button)
    bot.send_message(
        message.from_user.id,
        "Выберите срок прогноза",
        reply_markup=keyboard
    )


@bot.message_handler(
    func=lambda message: message.text in [
        "🕒3 часа",
        "🕕6 часов",
        "🕛12 часов",
        "🕐Завтра",
        "🕐Послезавтра"
    ],
    content_types=['text']
)
def send_forecast(message: object) -> None:
    """
    Отправляет пользователю прогноз на выбранный срок.
    :param message: объект Message telegram API
    :type message: object
    """
    filehandler = FileHandler()
    data = filehandler.load_data_from_json()
    if message.from_user.id == data[0]['user_id']:
        lat = data[0]['lat']
        lon = data[0]['lon']
        city_type = data[0]['city_type']
        city_name = data[0]['city_name']
    forecast_handler = WeatherAPIHandler(lat, lon)
    forecasts_data = forecast_handler.get_forecast()

    match message.text:
        case "🕒3 часа":
            forecast_time = 3 * 60 * 60
        case "🕕6 часов":
            forecast_time = 6 * 60 * 60
        case "🕛12 часов":
            forecast_time = 12 * 60 * 60
        case "🕐Завтра":
            forecast_time = 24 * 60 * 60
        case "🕐Послезавтра":
            forecast_time = 72 * 60 * 60

    utc_offset = forecasts_data["city"]["timezone"]
    forecast_target_time = message.date + forecast_time + utc_offset


    for i, item in enumerate(forecasts_data["list"]):
        if forecasts_data["list"][i]["dt"] < forecast_target_time < forecasts_data["list"][i + 1]["dt"]:
            temperature = int(
                round(
                    forecasts_data["list"][i]["main"]["temp"], 0
                )
            )
            feels_like = int(
                round(
                    forecasts_data["list"][i]["main"]["feels_like"], 0
                )
            )
            weather_condition = forecasts_data["list"][i]["weather"][0]["description"]
            weather_condition_icon = forecast_handler.get_weather_icon()

    reply = f"Прогноз погоды в {city_type}.{city_name}:\n" \
            f"{weather_condition_icon}{weather_condition.capitalize()}\n" \
            f"<b>Температура: </b>{temperature}°C\n" \
            f"<b>Ощущается как: </b>{feels_like}°C\n" \

    bot.send_message(message.from_user.id, reply, parse_mode="html")


# # обработка отправки пользователем названия города вручную
# @bot.message_handler(
#     func=lambda message: message.text not in ['⏰Прогноз', '◀️Назад'],
#     content_types=['text']
# )
# def send_current_weather_by_city(message):
#         city = message.text.capitalize()
#         city_data_api_handler = DadataAPIHandler(city=city)
#         city_coords = city_data_api_handler.get_coords_by_city()
#         if city_coords["result"] is None:
#             bot.send_message(message.from_user.id, "Такой город не найден")
#         else:
#             lat = city_coords["geo_lat"]
#             lon = city_coords["geo_lon"]
#             city_type = city_coords["region_type"]
#             city_name = city_coords["region"]
#
#             weather_api_handler = WeatherAPIHandler(lat, lon)
#             weather_data = weather_api_handler.get_current_weather()
#             temperature: int = int(round(weather_data["main"]["temp"], 0))
#             feels_like: int = int(round(weather_data["main"]["feels_like"], 0))
#             weather_condition = weather_data["weather"][0]["description"]
#             weather_condition_icon = weather_api_handler.get_weather_icon()
#
#             reply = f"Погода в {city_type}.{city_name} сейчас:\n" \
#                     f"{weather_condition_icon}{weather_condition.capitalize()}\n" \
#                     f"<b>Температура: </b>{temperature}°C\n" \
#                     f"<b>Ощущается как: </b>{feels_like}°C"
#
#         return bot.send_message(message.from_user.id, reply, parse_mode="html")


if __name__ == "__main__":
    bot.infinity_polling()
