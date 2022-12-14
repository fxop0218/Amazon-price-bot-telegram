from pymongo import MongoClient
from dotenv import load_dotenv
from amazon_scrap import scrap_amz_product
from datetime import datetime, date
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


def add_product(url, name, price, stars):
    time = datetime.now()
    try:
        product = {"_id": url, "name": name, "first_price": price, "last_price": price, "stars": stars, "last_update": time}
        products_collection.insert_one(product)
        print(f"Product added with link {url}")
        return True
    except Exception:
        print("Error")
        return False

def get_product(url):
    try:
        product = products_collection.find_one({"_id": url})
        if product is None:
            print("User without products")
            return "Error"
        print(f"Getted product: {product}")
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
        if products is None:
            print("User without products")
            return "Error"
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

        add_product(product_url, product["title"], product["price"], product["strs"])
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

# Remove a product of the user with this ID
def remove_user_product(user, product_id):
    try:
        products = get_user_products(user)
        print(f"Product id {product_id} to delete: { products[int(product_id)]}")
        user_collection.update_one({"_id": user}, {"$pull": {"products": products[int(product_id)]}})
        print("Deleted")
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
        print(user)
        products = get_user_products(user)
        print(f"Products: {products}")
        print(f"Product {id}, {products[int(id)]}")
        product = get_product(products[int(id)])

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

def update_price():
    all_proudcts = products_collection.find({})
    # Call scrapper
    time = datetime.now()
    if len(all_proudcts) > 0:
        for i in range(0, len(all_proudcts)):
            prod_features = scrap_amz_product(all_proudcts[i]["_id"])
            products_collection.update_one({"_id": all_proudcts[i]["_id"]}, {"last_price" : product["price"], "last_update": time})
    print("Not products to update")

#add_product("url", "name", 10, 3, 1)
#r = get_product("url")
