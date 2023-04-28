import json

import requests
from config import YW_API_KEY

URL = 'https://api.weather.yandex.ru/v2/informers?lat=55.75222&lon=37.61556&[lang=ru_RU]'

HEADERS = {'X-Yandex-API-Key': YW_API_KEY}

def get_weather():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return "Проблема с сервисом погоды"
