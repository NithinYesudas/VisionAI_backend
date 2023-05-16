from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

client = MongoClient(
    os.getenv("MONGODB_URL"))
db = client["vision_ai"]

def get_one_data(key:dict,collection:str):
    collection = db[collection]
    result = collection.find_one(key)
    return result
def insert_one_data(data:dict,collection:str):
    collection = db[collection]
    result = collection.insert_one(data)

