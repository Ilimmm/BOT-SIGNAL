from telegram import Bot
import asyncio

# Замените на ваш токен бота
BOT_TOKEN = '7545398584:AAFcd88RjWIU4UxdXNN2EEtTlpfTPRmT0v8'

async def set_webhook():
    bot = Bot(token=BOT_TOKEN)
    webhook_url = 'https://hydra-python.onrender.com'  # Замените на ваш реальный URL
    await bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    asyncio.run(set_webhook())
