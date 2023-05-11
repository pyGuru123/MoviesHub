import os
import re
import json
import asyncio
import telegram
from bson import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from app.utils import fetch_posts, random_post, aeshash

from app import collection_obj
from app.model import Movie


BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_CHANNEL = os.getenv("PUBLIC_CHANNEL")
PRIVATE_CHANNEL = os.getenv("PRIVATE_CHANNEL")
BIN_CHANNEL = os.getenv("BIN_CHANNEL")

def get_movie_url(name, url):
    try:
        fetch_posts()
        f = open("posts.json", "r")
        json_data = json.load(f)
        json_data = json.loads(json_data)
        content = json_data["feed"]["entry"]

        random_post_link = random_post(content)
        shorten_link = aeshash(random_post_link, name, url)

        return shorten_link

    except Exception as e:
        print(e)


def insert_to_db(data):
    img_url = data["image_url"]
    caption = data["caption"]
    text480p, url480p, text720p, url720p, text1080p, url1080p = "","","","","",""
    for button in data["buttons"]:
        if "480p" in button[0] and button[1]:
            text480p, url480p = button[0], button[1]
        elif "720p" in button[0] and button[1]:
            text720p, url720p = button[0], button[1]
        elif "1080p" in button[0] and button[1]:
            text1080p, url1080p = button[0], button[1]

    movie = Movie(img_url, caption, text480p, url480p, text720p, url720p, text1080p, url1080p)
    movie.save()

def convert_document(document):
    document['_id'] = str(document['_id'])
    return document

def get_movie_detail(caption):
    if caption:
        pattern = r'\d{4}'
        year = re.findall(pattern, caption)[-1]
        name = caption.split(year)[0].strip("(").strip()
        detail = (year + caption.split(year)[1].strip(")")).strip()
        return name, detail

def fetch_from_db(name):
    pattern = f".*{name}.*"
    query = {"caption": {"$regex": pattern, "$options": "i"}}
    matching_documents = collection_obj.find(query)

    results = []
    for document in matching_documents:
        document = convert_document(document)
        name, detail = get_movie_detail(document["caption"])
        document["name"] = name
        document["detail"] = detail
        results.append(document)

    return results


async def send_post(data):
    bot = telegram.Bot(token=BOT_TOKEN)
    
    image_url = data["image_url"]
    caption = data["caption"]
    buttons = data["buttons"]

    row1 = []
    row2 = []
    for button in buttons[:2]:
        row1.append(InlineKeyboardButton(button[0], url=button[1]))
    if len(buttons) == 3:
        row2.append(InlineKeyboardButton(buttons[2][0], url=buttons[2][1]))

    if len(buttons) <= 2:
        reply_markup = InlineKeyboardMarkup([row1])
    elif len(buttons) == 3:
        reply_markup = InlineKeyboardMarkup([row1, row2])

    chat_ids = [PUBLIC_CHANNEL, PRIVATE_CHANNEL]

    for _id in chat_ids:
        await bot.send_photo(
            chat_id=_id,
            photo=image_url,
            caption=caption,
            reply_markup=reply_markup,
            read_timeout=30,
            pool_timeout=30,
            connect_timeout=30,
            write_timeout=30,
        )

    insert_to_db(data)


# def get_all_posts():
#     bot = telegram.Bot(token=BOT_TOKEN)
#     try:
#         chat = bot.get_chat(chat_id=BIN_CHANNEL)
#     except TelegramError as e:
#         print(f'Error: {e}')
#         chat = []

#     if chat is not None:
#         messages = bot.get_messages(chat_id=chat.id)
#     else:
#         messages = []

#     return json.stringify(messages)