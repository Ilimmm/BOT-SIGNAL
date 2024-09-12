from fastapi import FastAPI, Request
from pydantic import BaseModel
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Создайте экземпляр FastAPI
app = FastAPI()

# Настройка Telegram бота
BOT_TOKEN = '7545398584:AAFcd88RjWIU4UxdXNN2EEtTlpfTPRmT0v8'
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Ваш Telegram бот код (из предыдущего сообщения)
async def start(update: Update, context):
    # (Код функции start)
    pass

async def button(update: Update, context):
    # (Код функции button)
    pass

async def handle_message(update: Update, context):
    # (Код функции handle_message)
    pass

# Обработчики для Telegram
application.add_handler(CommandHandler('start', start))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Настройка вебхуков для бота
@app.post("/webhook")
async def webhook(request: Request):
    json_str = await request.body()
    update = Update.de_json(json_str, application.bot)
    application.process_update(update)
    return {"status": "ok"}

# Запуск Uvicorn сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
