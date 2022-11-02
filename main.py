# Lib
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram import User
from dotenv import load_dotenv
from amazon_scrap import check_existence
from database import add_user_products
import os

load_dotenv()

AMAZON_ES_LINK = "https://www.amazon.es/"

updater = Updater(os.getenv("TELEGRAM_API_KEY"), use_context = True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(f'Amazon price traker🤖\n-----------------------\n /start to get info \n /help to get help \n /add_product to get product')


def add_product(update: Update, context: CallbackContext):
    text = update.message.text
    command = "/add_product"
    text = text.replace(command, "")

    if len(text) > 0:
        if AMAZON_ES_LINK in text:
            correct = check_existence(text)
            if correct:
                add_user_products(update.message.from_user.username, text)
                update.message.reply_text(f"✔✔Product with link: {text} added correctly ✔✔")
            else:
                update.message.reply_text(f"Link error😢")

            update.message.reply_text(f"The url is {correct}")
        else:
            update.message.reply_text(f"Juan text")
    else:
        update.message.reply_text(f"Introduce link of the amazon product")

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(f"🧠't?")

def unknown_msg(update: Update, context: CallbackContext):
    update.message.reply_text(f"{update.message.text} isn't valid 🤷‍♂️")

def dev(update: Update, context: CallbackContext):
    update.message.reply_text("Dev tools")
    user_id = update.message.from_user.username
    update.message.reply_text(f"User id: {user_id}")
## print(os.getenv("TELEGRAM_API_KEY"))
#

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('add_product', add_product))
updater.dispatcher.add_handler(CommandHandler('dev', dev))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_msg))

updater.start_polling()