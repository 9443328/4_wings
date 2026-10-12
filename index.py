import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, Update

# Подтягиваем токен из настроек Vercel
TOKEN = os.getenv("BOT_TOKEN", "8807378632:AAHHbPcfAJtjUy1K9ImLb0zEu5mKh6PoC-8")
bot = Bot(token=TOKEN)
dp = Dispatcher()

MY_TEXT = "Great. Now take the parameters from the previous image, multi"

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(MY_TEXT)

@dp.message(F.text)
async def any_text(message: Message):
    await message.answer(MY_TEXT)

# Vercel автоматически ищет асинхронную функцию handler/app/application
async def app(request):
    if request.method == "POST":
        try:
            json_data = await request.json()
            update = Update.model_validate(json_data, context={"bot": bot})
            await dp.feed_update(bot, update)
            return {"status": "ok"}
        except Exception as e:
            return {"status": f"error: {e}"}, 500
    return {"status": "Method Not Allowed"}, 405
