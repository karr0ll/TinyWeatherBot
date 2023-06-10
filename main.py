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
dp = Dispatcher()
user_shared_location = []


@dp.message(Command("start"))
async def get_geolocation_data(message: types.Message):
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

# TODO: добавить получение города с ввода пользователя


@dp.message(F.location)
async def send_forecast(message: types.Message):
    lat: float = message.location.latitude
    lon: float = message.location.longitude

    weather_api_handler = WeatherAPIHandler(lat, lon)
    weather_data = weather_api_handler.get_weather()

    city_data_api_handler = DadataAPIHandler(lat, lon)
    city_data = city_data_api_handler.get_city_data_by_coords()

    temperature = weather_data["fact"]["temp"]
    feels_like = weather_data["fact"]["feels_like"]

    # for item in city_data:
    city_type = city_data[0]["data"]["region_type"]
    city_name = city_data[0]["data"]["region"]

    reply = f"Погода в {city_type}.{city_name} сейчас:\n" \
            f"<b>Температура: </b>{temperature}°C\n" \
            f"<b>Ощущается как: </b>{feels_like}°C"

    await message.answer(reply)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
