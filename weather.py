from urllib import response
from dotenv import load_dotenv; load_dotenv()
import requests
import os

API_KEY = os.getenv("WEATHER_API_KEY")
URL_WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
UNITS_METRIC ="metric"
LANG_RU = "ru"

def get_weather_data(city):
    try:
        return requests.get(URL_WEATHER_API,
                        params={"q": city, "appid": API_KEY,
                                "units": UNITS_METRIC, "lang": LANG_RU})
    except requests.exceptions.RequestException:
        return None

def get_weather(city):
    response = get_weather_data(city)

    if response is None:
        return "Сервис недоступен"
    else:
        try:
            data = response.json()
        except ValueError:
            return "Ошибка: сервер вернул не JSON"

        if response.status_code == 200:
            return (f"Погода в {data['name']}: {data['weather'][0]['description']}, "
                    f"{data['main']['temp']:.1f}°C, ощущается как {data['main']['feels_like']},"
                    f"ветер {data['wind']['speed']} м/с")
        elif response.status_code == 404:
            return "Город не найден"
        elif response.status_code == 401:
            return f"Ошибка: {data['message']}"