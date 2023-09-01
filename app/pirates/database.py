import os
import pymongo
import platform
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

if platform.system() == "Windows":
    from dotenv import load_dotenv

    load_dotenv()

CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
DATABASE = os.environ.get("DATABASE")
COLLECTION = os.environ.get("COLLECTION")

client = pymongo.MongoClient(CONNECTION_STRING)
db = client[DATABASE]
collection = db[COLLECTION]


async def search_movie(movie):
    pattern = f".*{movie}.*"
    return list(collection.find({"caption": {"$regex": pattern, "$options": "i"}}))
