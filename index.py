import asyncio
import json
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, Update
from http.server import BaseHTTPRequestHandler

# Инициализируем бота. Токен берется из переменных окружения Vercel
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

# Специальный класс-обработчик, который Vercel ожидает от Python скриптов
class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Читаем JSON от Telegram
            json_data = json.loads(post_data.decode('utf-8'))
            update = Update.model_validate(json_data, context={"bot": bot})
            
            # Принудительно запускаем асинхронное событие aiogram внутри Serverless-сессии
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(dp.feed_update(bot, update))
            loop.close()
            
            # Отвечаем серверу Telegram, что запрос успешно обработан
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Бот-сервер работает!")
