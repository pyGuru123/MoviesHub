import os
import flask
from pymongo import MongoClient
from app import collection_obj

class Movie:
    def __init__(self, img_url, caption, text480p, url480p, text720p, url720p, text1080p, url1080p):
        self.img_url = img_url
        self.caption = caption
        self.text480p = text480p
        self.url480p  = url480p
        self.text720p  = text720p
        self.url720p  = url720p
        self.text1080p  = text1080p
        self.url1080p  = url1080p

    def to_dict(self):
        return {
            "img_url" : self.img_url,
	        "caption" : self.caption,
	        "text480p" : self.text480p,
	        "url480p" : self.url480p,
	        "text720p" : self.text720p,
	        "url720p" : self.url720p,
	        "text1080p" : self.text1080p,
	        "url1080p" : self.url1080p
        }

    def save(self):
        collection = collection_obj
        movie_data = self.to_dict()
        result = collection.insert_one(movie_data)
        return result.inserted_id