import json

import requests

import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from config import TG_TOKEN, HEADERS


bot = Bot(token=TG_TOKEN, parse_mode="HTML")
dp = Dispatcher()
user_shared_location = []



@dp.message(F.location)
async def get_location_data(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude

    url = f'https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}&[lang=ru_RU]'
    response = requests.get(url, headers=HEADERS)
    weather_data = json.loads(response.text)

    if response.status_code == 200:
        temperature = weather_data["fact"]["temp"]
        feels_like = weather_data["fact"]["feels_like"]
        reply = f"Привет,\nПогода в ???:\n" \
                f"<b>Температура: </b>{temperature}°C\n" \
                f"<b>Ощущается как: </b>{feels_like}°C"
        await message.answer(reply)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
