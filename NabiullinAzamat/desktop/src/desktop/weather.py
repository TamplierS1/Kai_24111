import json
import urllib.parse
from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_TOKEN = getenv("OPENWEATHERMAP_API_TOKEN")


class Weather:
    description: str
    temp: str
    feels_like: str
    wind_speed: str
    name: str

    def __init__(
        self, description: str, temp: str, feels_like: str, wind_speed: str, name: str
    ):
        self.description = description
        self.temp = temp
        self.feels_like = feels_like
        self.wind_speed = wind_speed
        self.name = name


def get_weather(city_name: str) -> Weather | None:
    if not city_name:
        print("Название города пустое")
        return None

    # Кодируем название города для безопасной передачи в URL (например, пробелы станут %20)
    encoded_city_name = urllib.parse.quote(city_name)

    # Конвертируем название города в координаты
    response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={encoded_city_name}&limit={1}&appid={WEATHER_API_TOKEN}"
    )
    geocoding = response.json()

    # Проверка, что город найден
    if len(geocoding) == 0:
        print(f"Город не найден: {response.text}")
        return None

    geocoding = geocoding[0]
    lat = geocoding["lat"]
    lon = geocoding["lon"]

    print(f"Geocoding object: {json.dumps(geocoding, indent=4)}")

    # Используем найденные координаты, чтобы получить погоду
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={'metric'}&lang={'ru'}&appid={WEATHER_API_TOKEN}"
    )
    if not response.ok:
        print(f"Weather request failed: {response.text}")
        return None

    weather = response.json()

    print(f"Weather object: {json.dumps(weather, indent=4)}")

    # Безопасное получение названия (если "ru" нет, берем оригинальное name или то, что ввел пользователь)
    display_name = geocoding.get("local_names", {}).get(
        "ru", geocoding.get("name", city_name)
    )

    return Weather(
        weather["weather"][0]["description"],
        weather["main"]["temp"],
        weather["main"]["feels_like"],
        weather["wind"]["speed"],
        display_name,
    )
