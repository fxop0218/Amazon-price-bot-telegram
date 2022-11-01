from pymongo import MongoClient
from dotenv import load_dotenv
import os

DATABASE = "amazonBot"
COLLECTION = "users"

load_dotenv()
print(os.getenv("MONGO_URI"))

# Client
client = MongoClient(os.getenv("MONGO_URI"))
db = client[DATABASE]
productsCollection = db[COLLECTION]

def user_command(user):
    print("hola")