import logging
import os


from dotenv import load_dotenv

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Шо ти {update.effective_user.first_name}')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hello_options = ['привіт', 'добрий день', 'здоров']
    goodbye_options = ['папа', 'допобачення']
    message = update.message.text.lower()


    reply_text = None
    for hello_option in hello_options:
        if hello_option in message:
            reply_text = f'{hello_option.capitalize()}, {update.effective_user.first_name} {update.effective_user.last_name}!'
            break

    for goodbye_option in goodbye_options:
        if goodbye_option in message:
            last_name = update.effective_user.last_name
            if last_name is None:
                reply_text = f'{goodbye_option.capitalize()}, {update.effective_user.first_name}!'
            else:
                reply_text = f'{goodbye_option.capitalize()}, {update.effective_user.first_name} {last_name}!'
            break

    if reply_text is None:
        reply_text = 'Я тебе не розумію'


    await update.message.reply_text(reply_text)


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


app.run_polling()


