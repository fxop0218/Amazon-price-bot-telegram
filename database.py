from pymongo import MongoClient
from dotenv import load_dotenv
from amazon_scrap import scrap_amz_product
import os

DATABASE = "amazonBot"
USERS = "users"
PRODUCTS = "products"

load_dotenv()
print(os.getenv("MONGO_URI"))
# Client
client = MongoClient(os.getenv("MONGO_URI"))
db = client[DATABASE]
products_collection = db[PRODUCTS]
user_collection = db[USERS]

def user_command(user):
    print("Exemple code")


def add_product(url, name, price, stars, last_update):
    try:
        product = {"_id": url, "name": name, "price": [price], "stars": stars, "last_update": last_update}
        products_collection.insert_one(product)
        return True
    except Exception:
        print("Error")
        return False

def get_product(url):
    try:
        product = products_collection.find({"_id": url})
        print(product[0])
        return product
    except Exception:
        print("Error")
    return "Error"
def user_exists(user):
    try:
        user_collection.find_one({"_id": user})
        return True
    except Exception:
        return False
def add_user(user):
    user = {"_id": user}
    user_collection.insert(user)
    return user

def get_user(user):
    try:
        user = user_collection.find_one({"_id": user})
        return user
    except Exception:
        print("Error")
        return "Error"

def get_user_products(user):
    try:
        products = user_collection.find_one({"_id": user}, {"products": 1})
        return products
    except Exception:
        print("Error")
    return "Error"

def add_user_products(user, product_url):
    product_ex = False
    # Check if the user exists
    user_ex = user_exists(user)
    # Add the user to db if the user don't exists
    if not user_ex:
        add_user(user)

    # if don't find the product
    try:
        product_url.find_one({"_id": product_url})
        product_ex = True
    except Exception:
        print("Creating the product")

    # Check if the product exists
    if product_ex:
        user_collection.update({"_id": user}, {"$push": {"products": product_url}})
    else:
        # Call scraper to get the data
        title, price, strs = get_product(product_url)
        last_update = ""
        result = add_product(product_url, name, price, stars, last_update)
        if result:
            print("Object created")
            try:
                user_collection.update({"_id": user}, {"$push": {"products" : product_url}})
            except Exception:
                print("User error")
                return False
        else:
            pritn("Error to create the product")
    return True

def remove_user_product(user, product_url):
    try:
        user_collection.update({"_id": user}, {"$pull": product_url})
        return True
    except Exception:
        return False

#add_product("url", "name", 10, 3, 1)
#r = get_product("url")
