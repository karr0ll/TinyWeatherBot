import json
import os

import requests
from dotenv import load_dotenv


class WeatherAPIHandler:
    load_dotenv()
    open_weather_api_key: str = os.environ.get("OPEN_WEATHER_API_KEY")

    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    def get_current_weather(self):
        url = f'https://api.openweathermap.org/data/2.5/weather?' \
              f'lat={self.lat}' \
              f'&lon={self.lon}' \
              f'&units=metric'\
              f'&lang=ru'\
              f'&appid={self.open_weather_api_key}'

        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return response.text
    def get_weather_icon(self):
        weather_data_for_icon = self.get_current_weather()
        weather_condition = weather_data_for_icon["weather"][0]["main"]
        if weather_condition == "Thunderstorm":
            return "⛈️"
        if weather_condition == "Drizzle" or weather_condition == "Rain":
            return "🌧️"
        if weather_condition == "Snow":
            return "❄️"
        if weather_condition == "Atmosphere":
            return "🌫️"
        if weather_condition == "Clear":
            return "☀️"
        if weather_condition == "Clouds":
            return "☁️"


    def get_forecast(self):
        url = f'https://api.openweathermap.org/data/2.5/forecast?' \
                f'lat={self.lat}' \
                f'&lon={self.lon}' \
                f'&units=metric' \
                f'&lang=ru' \
                f'&appid={self.open_weather_api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return response.text




# data = WeatherAPIHandler(55.7522200, 37.6155600)
# weather_data = data.get_current_weather()
# print(weather_data)
