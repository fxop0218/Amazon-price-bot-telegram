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
        product = {"_id": url, "name": name, "first_price": price, "last_price": price, "stars": stars, "last_update": last_update}
        products_collection.insert_one(product)
        print(f"Product added with link {url}")
        return True
    except Exception:
        print("Error")
        return False

def get_product(url):
    try:
        product = products_collection.find_one({"_id": url})
        print(f"Product: {product}")
        return product
    except Exception as e:
        print(f"Error to get product \n{e}")
    return "Error"

def user_exists(user):
    try:
        user2 = user_collection.find_one({"_id": user})
        if user2 is None:
            return False
        return True
    except Exception:
        return False
def add_user(user):
    user = {"_id": user}
    user_collection.insert_one(user)
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
        products = user_collection.find_one({"_id": user}, {"_id": 0, "products": 1})
        #print(products)
        return products["products"]
    except Exception:
        print("Error")
    return "Error"

def add_user_products(user, product_url):
    already_have = False
    # Check if the user exists
    user_ex = user_exists(user)
    # Add the user to db if the user don't exists
    if not user_ex:
        add_user(user)

    # if don't find the product
    try:
        prod_ex = product_exists(product_url)
    except Exception:
        prod_ex = False
        print("Creating the product")

    print(prod_ex)
    # Check if the product exists
    if not prod_ex:
        # Call scraper to get the data
        product = scrap_amz_product(product_url)
        last_update = "today"

        add_product(product_url, product["title"], product["price"], product["strs"], last_update)
        print("Object created")
        already_have = False
    else:
        usr_products = get_user_products(user)
        for usr_prod in usr_products:
            if usr_prod == product_url:
                already_have = True

    # TODO comporbate if this user have the product
    print(already_have)
    if not already_have:
        user_collection.update_one({"_id": user}, {"$push": {"products" : product_url}}, upsert = True)
        print("Object added to the user")
        return True
    print(f"Also have the product")
    return True

def remove_user_product(user, product_url):
    try:
        user_collection.findOneAndUpdate({"_id": user}, {"$pull": product_url})
        return True
    except Exception:
        return False

def get_all_products(user):
    text = ""
    try:
        product = get_user_products(user)
        if len(product) <= 0:
            return "No products added"
        for p in range(0, len(product)):
            print(text)
            text = text + f"\n Product id: {p} product link: {product[p]}"
    except Exception:
        print("Exception")
    return text

def get_all_products_name(user):
    text = ""
    try:
        user_products = get_user_products(user)
        print(len(user_products))
        if len(user_products) <=0:
             return "No products added"
        for p in range(0, len(user_products)):
            id = user_products[p]
            print(f"Id: {id}")
            product = get_product(id)
            print(product)
            text = text + f"ID: {p} Name: {product['name'][:50]}...\n"
            print(text)
    except Exception as e:
        print(e)
    return text

def get_one_product(user, id):
    try:
        products = get_user_products(user)
        pritn(f"Products: {products}")
        product = get_product(products[id])
        pritn(f"Products: {product}")

        if product is None:
            return "Error"
        return product
    except Exception:
        return "Error"



def product_exists(product):
    try:
        product_ob = products_collection.find_one({"_id": product})
        print(product_ob)
        if product_ob is None:
            return False
        return True
    except Exception:
        return None


#add_product("url", "name", 10, 3, 1)
#r = get_product("url")
