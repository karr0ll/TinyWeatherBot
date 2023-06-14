import asyncio
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv

from api_handlers.dadata_api_handler import DadataAPIHandler
from api_handlers.weather_api_handler import WeatherAPIHandler

load_dotenv()
tg_token: str = os.environ.get("TG_TOKEN")

bot = Bot(token=tg_token, parse_mode="HTML")
dispatcher = Dispatcher()
user_shared_location = []


@dispatcher.message(Command("start"))
async def ask_for_location(message: types.Message):
    buttons = [[types.KeyboardButton(
        text="Поделиться местоположением",
        request_location=True
    )]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Введите название города"
    )
    await message.answer("Отправьте свое местоположение или введите название города",
                         reply_markup=keyboard)


@dispatcher.message(F.text)
async def send_current_weather_by_city(message: types.Message):
    city = message.text.capitalize()
    city_data_api_handler = DadataAPIHandler(city=city)
    city_coords = city_data_api_handler.get_coords_by_city()
    if city_coords["result"] is None:
        await message.answer("Такой город не найден")
    else:
        lat = city_coords["geo_lat"]
        lon = city_coords["geo_lon"]
        city_type = city_coords["region_type"]
        city_name = city_coords["region"]

        weather_api_handler = WeatherAPIHandler(lat, lon)
        weather_data = weather_api_handler.get_weather()
        temperature = weather_data["fact"]["temp"]
        feels_like = weather_data["fact"]["feels_like"]

        reply = f"Погода в {city_type}.{city_name} сейчас:\n" \
                f"<b>Температура: </b>{temperature}°C\n" \
                f"<b>Ощущается как: </b>{feels_like}°C"
        await message.answer(reply)

@dispatcher.message(F.location)
async def send_current_weather_by_location(message: types.Message):
    lat: float = message.location.latitude
    lon: float = message.location.longitude

    weather_api_handler = WeatherAPIHandler(lat, lon)
    weather_data = weather_api_handler.get_weather()

    city_data_api_handler = DadataAPIHandler(lat=lat, lon=lon)
    city_data = city_data_api_handler.get_city_data_by_coords()

    temperature = weather_data["fact"]["temp"]
    feels_like = weather_data["fact"]["feels_like"]

    city_type = city_data[0]["data"]["region_type"]
    city_name = city_data[0]["data"]["region"]

    reply = f"Погода в {city_type}.{city_name} сейчас:\n" \
            f"<b>Температура: </b>{temperature}°C\n" \
            f"<b>Ощущается как: </b>{feels_like}°C"

    await message.answer(reply)


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
