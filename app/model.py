import os
import flask
from pymongo import MongoClient
from app import collection_obj

class Movie:
    def __init__(self, caption, size, chat_id, msg_id, file_unique_id):
        self.caption = caption
        self.size = size
        self.chat_id  = chat_id
        self.msg_id  = msg_id
        self.file_unique_id = file_unique_id

    def to_dict(self):
        return {
            "caption" : self.caption,
            "size" : self.size,
            "chat_id" : self.chat_id,
            "message_id" : self.msg_id,
            "file_unique_id": self.file_unique_id
        }

    def save(self):
        collection = collection_obj
        movie_data = self.to_dict()
        result = collection.insert_one(movie_data)
        return result.inserted_id