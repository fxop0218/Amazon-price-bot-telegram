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
from database import add_user_products, get_one_product, get_all_products, get_product, get_user, get_user_products, product_exists, get_all_products_name, remove_user_product
import os
import operator

load_dotenv()

AMAZON_ES_LINK = "https://www.amazon.es/"

updater = Updater(os.getenv("TELEGRAM_API_KEY"), use_context = True)

def help(update: Update, context: CallbackContext):
    update.message.reply_text(f'Amazon price traker🤖\n-----------------------\n/help to get help \n/add_product [link] Add the product in your list \n/all_products Show all your products use [/all_products sl] to show the products with the link\n/product [id] Informatión of the product with this id, to check the id use /all_products\n/remove [id] to remove the product')

def start(update: Update, context: CallbackContext):
    update.message.reply_text(f"Wellcome to Amazon price traker telegram bot🤖\nThis bot is created by Francesc Oliveras 😁 to get more information of the creator use /info \n To start using the bot, use /hel to check all the commands.")

def info(update: Update, context: CallbackContext):
    update.message.reply_text(f"Linkedin📩: www.linkedin.com/in/francesc-oliveras-perez\nKaggle: https://www.kaggle.com/francescoliveras\nGitHub: https://github.com/fxop0218")
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
        if objects is None or objects == "":
            update.message.reply_text("You don't have products in your list")
        else:
            print(f"Sowing {len(objects)} with link")
            update.message.reply_text(objects)
    # Show with name
    else:
        objects = get_all_products_name(user_id)
        if objects is None or objects == "":
            update.message.reply_text("You don't have any object registred")
        else:
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
        print(product)
        if product != "Error":
            update.message.reply_text(f"Product: {product['name']}\nFirst price: {product['first_price']}€\nLast price: {product['last_price']}€\nPrice dif: {float(product['first_price'].replace(',','.')) - float(product['last_price'].replace(',','.'))}\nStars: {product['stars']}\nLast update: {product['last_update'].strftime('%d/%m/%y')}")
        else:
            update.message.reply_text("Value out of bounds")


def remove_product(update: Update, context: CallbackContext):
    comand = "/remove "
    user = update.message.from_user.username
    product_id = update.message.text
    if len(product_id) <=0:
        update.message.reply_text("Put a index /remove [index]")
    else:
        product_id = product_id.replace(comand, "")
        if product_id.isnumeric():
            removed = remove_user_product(user, product_id)
            if removed:
                update.message.reply_text("Product successfully deleted")
            else:
                update.message.reply_text("Error to delete the product, or inexistent product")
        else:
            update.message.reply_text(f"{product_id} is not a number 🤨🤨🤨🤨")

# Unknow comands and msg
def unknown(update: Update, context: CallbackContext):
                update.message.reply_text(f"🧠't?")

def unknown_msg(update: Update, context: CallbackContext):
    update.message.reply_text(f"{update.message.text} isn't valid 🤷‍♂️")



## print(os.getenv("TELEGRAM_API_KEY"))
#

updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('add_product', add_product))
updater.dispatcher.add_handler(CommandHandler('dev', dev))
updater.dispatcher.add_handler(CommandHandler('info', info))
updater.dispatcher.add_handler(CommandHandler('remove', remove_product))
updater.dispatcher.add_handler(CommandHandler('all_products',show_products))
updater.dispatcher.add_handler(CommandHandler('product',show_one_product))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_msg))

updater.start_polling()