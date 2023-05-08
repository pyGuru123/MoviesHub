import os
from flask import Flask
from config import Config
from pymongo import MongoClient

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
DATABASE = os.getenv("DATABASE")
COLLECTION = os.getenv("COLLECTION")

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

client = MongoClient(CONNECTION_STRING)
db = client[DATABASE]
collection_obj = db[COLLECTION]

from app import routes
