import os
import json
import platform
import requests
from math import ceil
from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

if platform.system() == "Windows":
    from dotenv import load_dotenv

    load_dotenv()

PIRATES_BOT_TOKEN = os.environ.get("PIRATES_BOT_TOKEN")
MOVIESHUB_CHANNEL = os.environ.get("MOVIESHUB_CHANNEL")

pirates_bot = Bot(token=PIRATES_BOT_TOKEN)

async def isSubscriberOfMoviesHub(user_id):
    try:
        isSubscriber = await pirates_bot.get_chat_member(chat_id=MOVIESHUB_CHANNEL, user_id=user_id)
        logger.info(isSubscriber.status)
        if isSubscriber.status in ["member", "creator", "admin"]:
            return True
    except NetworkError as ne:
        return True
    except Exception as e:
        logger.error(f"{e=}")
        return False

async def sendTextMessage(chat_id, text, reply_id):
    info = await pirates_bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_id)
    return info

async def copyFile(chat_id, from_chat_id, message_id):
    info = await pirates_bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)
    return info

async def sendKeyboard(chat_id, text, reply_id, reply_markup):
    info = await pirates_bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, 
                reply_to_message_id=reply_id)
    return info

async def editKeyboard(chat_id, text, reply_id, reply_markup):
    info = await pirates_bot.edit_message_text(chat_id=chat_id, text=text, reply_markup=reply_markup, 
                message_id=reply_id)
    return info

async def getJoinChannelKeyboard(text):
    keyboard = [
        [InlineKeyboardButton("Join Channel", url="https://t.me/movieshubmt")],
        [InlineKeyboardButton("Try Again", callback_data=text)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def populate_keyboard(documents, items_per_page, current_page):
    keyboard = []
    start_index = (current_page - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(documents))
    max_page = ceil(len(documents) / items_per_page)

    for document in documents[start_index:end_index]:
        text = f"{document['size']} {document['caption']}"
        callback_data = f"{document['chat_id']}@@{document['message_id']}"
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    prev_button = InlineKeyboardButton("Previous", callback_data="prev:prev")
    page_button = InlineKeyboardButton(f"{current_page}/{max_page}", callback_data="status")
    next_button = InlineKeyboardButton("Next", callback_data="next:next")
    keyboard.append([prev_button, page_button, next_button])

    return keyboard

async def getMoviesListKeyboard(documents, page=1, type=""):
    items_per_page = 8
    current_page = page
    max_page = ceil(len(documents) / items_per_page)
    keyboard = None

    if type == "next":
        if current_page < max_page:
            current_page += 1
            keyboard = await populate_keyboard(documents, items_per_page, current_page)
    if type == "prev":
        if current_page > 1:
            current_page -= 1
            keyboard = await populate_keyboard(documents, items_per_page, current_page)
    elif type == "":
        keyboard = await populate_keyboard(documents, items_per_page, current_page)

    if keyboard:
        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup, current_page

    return None, None
