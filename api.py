from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Dispatcher
import logging

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Инициализация FastAPI приложения
app = FastAPI()

# Инициализация бота
BOT_TOKEN = '7545398584:AAFcd88RjWIU4UxdXNN2EEtTlpfTPRmT0v8'
bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot=bot, update_queue=None)

@app.post("/webhook")
async def webhook(request: Request):
    json = await request.json()
    update = Update.de_json(json, bot)
    dispatcher.process_update(update)
    return {"status": "ok"}
