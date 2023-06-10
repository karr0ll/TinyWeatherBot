import os

from dotenv import load_dotenv

from dadata import Dadata


class DadataAPIHandler:

    def __init__(self, lat: float, lon: float) -> None:
        """
        Класс инициализируется координатами из геолокации пользователя и
        :param lat: широта
        :type lat: float
        :param lon: долгота
        :type lon: float
        """
        self.lat = lat
        self.lon = lon

    def get_city_data_by_coords(self) -> list[dict]:
        """
        Получает координаты пользователя и возвращает
        название города
        :return: спиок словарей с данными о города
        :rtype: list[dict]
        """
        load_dotenv()
        dadata_token: str = os.environ.get("DADATA_TOKEN")
        token = dadata_token
        dadata = Dadata(token)
        city_data = dadata.geolocate(
            name="address",
            lat=self.lat,
            lon=self.lon,
            radius_meters=500,
            count=1
        )
        return city_data
