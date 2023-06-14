import os

from dotenv import load_dotenv

from dadata import Dadata


class DadataAPIHandler:

    def __init__(
            self,
            lat: float = None,
            lon: float = None,
            city: str = None
    ) -> None:
        """
        Класс инициализируется координатами из геолокации пользователя и
        :param lat: широта
        :type lat: float
        :param lon: долгота
        :type lon: float
        """
        self.lat = lat
        self.lon = lon
        self.city = city

    def get_city_data_by_coords(self) -> list[dict]:
        """
        Получает координаты пользователя и возвращает
        название города
        :return: спиок словарей с данными о города
        :rtype: list[dict]
        """
        load_dotenv()
        DADATA_TOKEN: str = os.environ.get("DADATA_TOKEN")
        dadata = Dadata(DADATA_TOKEN)
        city_from_coords_data = dadata.geolocate(
            name="address",
            lat=self.lat,
            lon=self.lon,
            radius_meters=500,
            count=1
        )
        return city_from_coords_data

    def get_coords_by_city(self) -> dict:
        load_dotenv()
        DADATA_TOKEN: str = os.environ.get("DADATA_TOKEN")
        DADATA_SECRET: str = os.environ.get("DADATA_SECRET")
        dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)
        coords_from_city_data = dadata.clean(
            "address", self.city
        )
        return coords_from_city_data

