import json
import requests

from config import HEADERS
from main import user_shared_location


def get_weather():
    lat = user_shared_location[0]
    lon = user_shared_location[1]

    url = f'https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}&[lang=ru_RU]'

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return "Проблема с сервисом погоды"
