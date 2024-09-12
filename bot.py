from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

async def start(update: Update, context):
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

    if 'message_id' in context.chat_data:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=context.chat_data['message_id']
            )
        except Exception as e:
            print(f"Error deleting message: {e}")
        del context.chat_data['message_id']

    message = await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=welcome_text,
        parse_mode='HTML',
        reply_markup=reply_markup
    )
    context.chat_data['message_id'] = message.message_id

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = update.effective_user.id

    if 'message_id' in context.chat_data:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=context.chat_data['message_id']
            )
        except Exception as e:
            print(f"Error deleting message: {e}")
        del context.chat_data['message_id']

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

    elif data == 'get_signal':
        if 'registered_users' in context.chat_data and user_id in context.chat_data['registered_users']:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are successfully registered! You can now access the signals.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Open HYDRA SIGNALS", web_app=WebAppInfo(url='https://hydra-signal.onrender.com'))],
                    [InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]
                ])
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please complete registration and send your user ID or screenshot for confirmation.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]
                ])
            )

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

    elif data == 'main_menu':
        await start(update, context)

async def handle_message(update: Update, context):
    user_id = update.effective_user.id
    message = update.message.text

    if message.isdigit() and len(message) >= 8:
        if 'registered_users' not in context.chat_data:
            context.chat_data['registered_users'] = []
        context.chat_data['registered_users'].append(user_id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Thank you! You are now registered and can access the signals.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Open HYDRA SIGNALS", web_app=WebAppInfo(url='https://hydra-signal.onrender.com'))],
                [InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]
            ])
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please send a valid ID (at least 8 digits) or screenshot of your registration.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 MAIN MENU", callback_data='main_menu')]
            ])
        )

async def setup_bot():
    application = ApplicationBuilder().token('7545398584:AAFcd88RjWIU4UxdXNN2EEtTlpfTPRmT0v8').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await application.initialize()
    return application
