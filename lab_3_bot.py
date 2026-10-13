from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from weather import get_weather
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")


session = AiohttpSession(proxy=os.getenv("PROXY_IP"))
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Напиши мне название города, и я скажу погоду")

@dp.message()
async def handle_city(message: Message):
    await message.answer(get_weather(message.text))

async def main():
    await dp.start_polling(bot)

asyncio.run(main())