import os
import json
import random
import requests
from datetime import datetime


def download_posts():
    url = "https://moviehubm.blogspot.com/feeds/posts/summary?alt=json-in-script"
    r = requests.get(url)
    data = r.text
    json_data = data.strip("gdata.io.handleScriptLoaded(").strip(");")
    with open("posts.json", "w") as file:
        json.dump(json_data, file)


def fetch_posts():
    file_path = "posts.json"
    if not os.path.exists(file_path):
        download_posts()
    else:
        creation_time = os.path.getmtime(file_path)
        creation_datetime = datetime.fromtimestamp(creation_time)
        creation_date = creation_datetime.date()
        today = datetime.today().date()

        if today > creation_date:
            download_posts()


def random_post(content):
    links = []
    for i in range(0, len(content)):
        for j in range(0, len(content[i]["link"])):
            if content[i]["link"][j]["rel"] == "alternate":
                link = content[i]["link"][j]["href"]
                break
        links.append(link)

    randindex = random.random() * len(links)
    randindex = int(randindex)
    return links[randindex]


def aeshash(random_post_link, name, url):
    # https://dl.tgxlink.eu.org/dl/643ee970cd3343ba2a658fe4
    url_hash = ""
    for ch in url:
        url_hash += chr(ord(ch) + 1)
    result = f"{random_post_link}?name={name}&url={url_hash}"
    return result
