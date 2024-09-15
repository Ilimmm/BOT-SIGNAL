from fastapi import FastAPI, Request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.ext import ContextTypes
import os
from contextlib import asynccontextmanager
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание FastAPI приложения
app = FastAPI()

# Токен бота и создание объекта Bot
TOKEN = '7545398584:AAFcd88RjWIU4UxdXNN2EEtTlpfTPRmT0v8'  # Ваш токен бота
bot = Bot(token=TOKEN)

# Инициализация приложения Telegram
application = Application.builder().token(TOKEN).build()

# Определение обработчиков команд и сообщений
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo_url = 'https://i.postimg.cc/d3m8Lcpm/mines.jpg'
    welcome_text = """Welcome to 🔸MINES HYDRA🔸!
    
    💣Mines is a gambling game at the 1win betting office, based on the classic “Minesweeper”.
    Your goal is to open safe cells without triggering traps.

    <code>Our bot is powered by OpenAI's neural network.
    It can predict the location of stars with an 85% probability.</code>"""

    keyboard = [
        [InlineKeyboardButton("📝 REGISTRATION", callback_data='register'),
         InlineKeyboardButton("📚 INSTRUCTION", callback_data='instruction')],
        [InlineKeyboardButton("❗️ GET SIGNAL ❗️", callback_data='get_signal')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Удаление старого сообщения (если существует)
    if 'message_id' in context.chat_data:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=context.chat_data['message_id']
            )
            logging.info(f"Deleted old message with ID {context.chat_data['message_id']}")
        except Exception as e:
            logging.error(f"Error deleting message: {e}")
        del context.chat_data['message_id']

    # Отправка нового приветственного сообщения
    try:
        message = await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo_url,
            caption=welcome_text,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
        context.chat_data['message_id'] = message.message_id
        logging.info("Sent welcome photo message")
    except Exception as e:
        logging.error(f"Error sending welcome message: {e}")

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = update.effective_user.id

    # Удаление старого сообщения (если существует)
    if 'message_id' in context.chat_data:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=context.chat_data['message_id']
            )
            logging.info(f"Deleted old message with ID {context.chat_data['message_id']}")
        except Exception as e:
            logging.error(f"Error deleting message: {e}")
        del context.chat_data['message_id']

    # Обработка различных команд
    try:
        if data == 'register':
            registration_photo_url = 'https://i.postimg.cc/HWQ0Sbnc/registration.jpg'
            registration_text = """After registration, send your user ID to confirm.
            Then you will receive access to the signals!"""

            keyboard = [
                [InlineKeyboardButton("🔗 REGISTRATION", url='https://1wimdx.life/casino/list?open=register&p=dcau')],
                [InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            message = await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=registration_photo_url,
                caption=registration_text,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            context.chat_data['message_id'] = message.message_id
            logging.info("Sent registration photo message")

        elif data == 'get_signal':
            if 'registered_users' in context.chat_data and user_id in context.chat_data['registered_users']:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="You are successfully registered! You can now access the signals.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open HYDRA SIGNALS", web_app=WebAppInfo(url='https://hydra-signal.onrender.com'))],
                                                      [InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]])
                )
                logging.info("Sent signal access message")

            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Please complete registration and send your user ID or screenshot for confirmation.",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]])
                )
                logging.info("Sent registration reminder message")

        elif data == 'instruction':
            instruction_text = """The bot is based on and trained using OpenAI's neural network cluster 🖥[ChatGPT-v4].
            
            For training, the bot played 🎰over 8000 games.
            Currently, bot users successfully make 20-30% of their 💸capital daily!

            <code>The bot is still learning, and its accuracy is at 85%!</code>

            Follow these instructions for maximum profit:
            
            🔸 1. Register at the 1WIN betting office. If it doesn’t open - use a VPN (Sweden). I use VPN Super Unlimited Proxy.
            <code>Access to signals will not be available without registration!</code>

            🔸 2. Deposit funds into your account.

            🔸 3. Go to the 1win games section and select the 💣"MINES" game.

            🔸 4. Set the number of traps to three. This is important!

            🔸 5. Request a signal from the bot and place bets based on the bot’s signals.

            🔸 6. In case of a losing signal, we advise you to double (X2) your bet to fully cover the loss in the next signal."""

            keyboard = [[InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            message = await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=instruction_text,
                parse_mode='HTML',
                reply_markup=reply_markup
            )
            context.chat_data['message_id'] = message.message_id
            logging.info("Sent instruction message")

        elif data == 'main_menu':
            await start(update, context)
            logging.info("Returned to main menu")

    except Exception as e:
        logging.error(f"Error in button handler: {e}")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    message = update.message.text

    try:
        if message.isdigit() and len(message) >= 8:
            if 'registered_users' not in context.chat_data:
                context.chat_data['registered_users'] = []
            context.chat_data['registered_users'].append(user_id)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Thank you! You are now registered and can access the signals.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Open HYDRA SIGNALS", web_app=WebAppInfo(url='https://hydra-signal.onrender.com'))],
                                                  [InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]])
            )
            logging.info("Registered user and sent access message")
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please send a valid ID (at least 8 digits) or screenshot of your registration.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]])
            )
            logging.info("Sent invalid ID message")
    except Exception as e:
        logging.error(f"Error handling message: {e}")

# Добавление обработчиков в приложение Telegram
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Новый способ управления жизненным циклом
@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = "https://hydra-python.onrender.com/webhook"  # Ваш URL
    try:
        await application.initialize()
        await bot.set_webhook(webhook_url)
        logging.info("Webhook set")
        yield
    except Exception as e:
        logging.error(f"Error in lifespan: {e}")
    finally:
        await bot.delete_webhook()
        logging.info("Webhook deleted")

# Обновляем приложение FastAPI с использованием lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    logging.info("Received GET request at /")
    return {"message": "Telegram bot is running!"}

@app.post("/webhook")
async def webhook(request: Request):
    try:
        json_update = await request.json()
        update = Update.de_json(json_update, bot)
        await application.process_update(update)
        logging.info("Processed webhook update")
    except Exception as e:
        logging.error(f"Error processing webhook update: {e}")
    return {"status": "ok"}

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
