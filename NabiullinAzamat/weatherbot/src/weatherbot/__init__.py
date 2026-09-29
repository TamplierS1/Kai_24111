import asyncio
import json
import logging
import sys
from os import getenv

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
BOT_TOKEN = getenv("BOT_TOKEN")
WEATHER_API_TOKEN = getenv("OPENWEATHERMAP_API_TOKEN")
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Отправьте мне название любого города или геолокацию и я покажу вам соответствующую погоду."
    )


@dp.message(F.text)
async def city_name_handler(message: Message) -> None:
    # Конвертируем название города в координаты
    city_name = message.text
    response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={1}&appid={WEATHER_API_TOKEN}"
    )
    geocoding = response.json()
    if len(geocoding) == 0:
        logger.warning(f"Direct geocoding request failed: {response.text}")
        await message.answer(
            f"Ошибка! Не удалось получить погоду в городе: {city_name}"
        )
        return

    geocoding = geocoding[0]
    lat = geocoding["lat"]
    lon = geocoding["lon"]

    logger.info(f"Geocoding object: {json.dumps(geocoding, indent=4)}")

    # Используем найденные координаты, чтобы получить погоду
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={'metric'}&lang={'ru'}&appid={WEATHER_API_TOKEN}"
    )
    if not response.ok:
        logger.warning(f"Weather request failed: {response.text}")
        await message.answer(
            f"Ошибка! Не удалось получить погоду в городе: {city_name}"
        )
        return

    weather = response.json()
    description = weather["weather"][0]["description"]
    temp = weather["main"]["temp"]
    feels_like = weather["main"]["feels_like"]
    wind_speed = weather["wind"]["speed"]
    name = geocoding["local_names"]["ru"]

    logger.info(f"Weather object: {json.dumps(weather, indent=4)}")

    await message.answer(
        f"{name}\nОписание: {description}\nТемпература: {temp}\n"
        + f"Ощущается: {feels_like}\nСкорость ветра: {wind_speed}"
    )


@dp.message(F.location)
async def location_handler(message: Message) -> None:
    assert message.location is not None

    # Находим погоду по координатам, которые предоставил пользователь
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather"
        + f"?lat={message.location.latitude}&lon={message.location.longitude}"
        + f"&units={'metric'}&lang={'ru'}&appid={WEATHER_API_TOKEN}"
    )
    if not response.ok:
        logger.warning(f"Weather request failed: {response.text}")
        await message.answer("Ошибка! Не удалось получить погоду.")
        return

    weather = response.json()
    description = weather["weather"][0]["description"]
    temp = weather["main"]["temp"]
    feels_like = weather["main"]["feels_like"]
    wind_speed = weather["wind"]["speed"]

    logger.info(f"Weather object: {json.dumps(weather, indent=4)}")

    # Находим название города по координатам, которые предоставил пользователь
    response = requests.get(
        "http://api.openweathermap.org/geo/1.0/reverse?"
        + f"lat={message.location.latitude}&lon={message.location.longitude}"
        + f"&limit={1}&appid={WEATHER_API_TOKEN}"
    )
    geocoding = response.json()
    if len(geocoding) == 0:
        logger.warning(f"Reverse geocoding request failed: {response.text}")
        await message.answer("Ошибка! Не удалось получить погоду.")
        return

    geocoding = geocoding[0]
    name = geocoding["local_names"]["ru"]

    await message.answer(
        f"{name}\nОписание: {description}\nТемпература: {temp}\n"
        + f"Ощущается: {feels_like}\nСкорость ветра: {wind_speed}"
    )


@dp.message()
async def other_handler(message: Message) -> None:
    await message.answer("Ошибка! Пожалуйста отправьте название города или геолокацию.")


async def main() -> None:
    if BOT_TOKEN is None:
        logger.warning("no bot token found in environment.")
        return
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())
