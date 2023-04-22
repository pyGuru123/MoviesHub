import os
import json
import asyncio
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.utils import fetch_posts, random_post, aeshash


BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_CHANNEL = os.getenv("PUBLIC_CHANNEL")
PRIVATE_CHANNEL = os.getenv("PRIVATE_CHANNEL")
BIN_CHANNEL = os.getenv("BIN_CHANNEL")

bot = telegram.Bot(token=BOT_TOKEN)

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


async def send_post(data):
    print(data) 
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

    chat_ids = [PUBLIC_CHANNEL, PRIVATE_CHANNEL, BIN_CHANNEL]

    for _id in chat_ids:
        await bot.send_photo(chat_id=_id, photo=image_url, caption=caption, reply_markup=reply_markup)
