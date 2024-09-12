import asyncio
from telegram import Bot

BOT_TOKEN = '7545398584:AAFcd88RjWIU4UxdXNN2EEtTlpfTPRmT0v8'
WEBHOOK_URL = 'https://hydra-python.onrender.com/webhook'

async def set_webhook():
    bot = Bot(token=BOT_TOKEN)
    await bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    asyncio.run(set_webhook())
