import requests
from config import YW_API_KEY

URL = 'https://api.weather.yandex.ru/v2/informers?lat=55.75222&lon=37.61556&[lang=ru_RU]'

HEADERS = {'X-Yandex-API-Key': YW_API_KEY}

def get_weather():
    response = requests.get(URL, headers=HEADERS)
    api_status = response.status_code
    if api_status == 200:
        return response.text
    else:
        return "Проблема с сервисом погоды"

print(get_weather())

