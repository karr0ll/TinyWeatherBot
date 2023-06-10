import json
import os

import requests
from dotenv import load_dotenv


class WeatherAPIHandler:

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    def get_weather(self):
        load_dotenv()
        yw_api_key: str = os.environ.get("YW_API_KEY")
        header = {'X-Yandex-API-Key': yw_api_key}
        url = f'https://api.weather.yandex.ru/v2/informers?lat={self.lat}&lon={self.lon}&[lang=ru_RU]'

        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return "Проблема с сервисом погоды"
