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
from database import add_user_products, get_one_product, get_all_products, get_product, get_user, get_user_products, product_exists, get_all_products_name
import os
import operator

load_dotenv()

AMAZON_ES_LINK = "https://www.amazon.es/"

updater = Updater(os.getenv("TELEGRAM_API_KEY"), use_context = True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(f'Amazon price traker🤖\n-----------------------\n /start to get info \n /help to get help \n /add_product [link] Add the product in your list \n /all_products Show all your products\n /show_one_product [id] Get the product with this id')


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

# TODO add sl to show the link or not
def show_products(update: Update, context: CallbackContext):
    user_id = update.message.from_user.username
    command = "/all_products "
    show_link = update.message.text
    print(len(show_link))

    if len(show_link) > len(command):
        show_link = update.message.text.replace(command, "")
        print(show_link)
    # Show with link
    if operator.contains(show_link, "sl"):
        objects = get_all_products(user_id)
        print(f"Sowing {len(objects)} with link")
        update.message.reply_text(objects)
    # Show with name
    else:
        objects = get_all_products_name(user_id)
        print(f"Sowing {len(objects)} with name")
        update.message.reply_text(objects)

def  show_one_product(update: Update, contex: CallbackContext):
    command = "/product "
    id = update.message.text.replace(command, "")
    user_id = update.message.from_user.username
    print(f"Number: {id}")

    if not id.isnumeric():
        update.message.reply_text(f"{id} is not a number")
    else:
        product = get_one_product(user_id, id)
        if product != "Error":
            update.message.reply_text(f"Product {product['name']}, first price: {product['first_price']}, last price: {product['last_price']}, stars: {product['stars']}, last update: {product['last_update']}")
        else:
            update.message.reply_text("Value out of bounds")


## print(os.getenv("TELEGRAM_API_KEY"))
#

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('add_product', add_product))
updater.dispatcher.add_handler(CommandHandler('dev', dev))
updater.dispatcher.add_handler(CommandHandler('all_products',show_products))
updater.dispatcher.add_handler(CommandHandler('product',show_one_product))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_msg))

updater.start_polling()