import os
import json
import platform
import requests
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
        if isSubscriber:
            return True
    except Exception as e:
        logger.error(f"{e=}")
        return False

async def sendTextMessage(chat_id, text, reply_id):
    await pirates_bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_id)

async def copyFile(chat_id, from_chat_id, message_id):
    await pirates_bot.copy_message(chat_id=chat_id, from_chat_id=from_chat_id, message_id=message_id)

async def sendKeyboard(chat_id, text, reply_id, reply_markup):
    await pirates_bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup, 
                reply_to_message_id=reply_id)

async def getJoinChannelKeyboard(text):
    keyboard = [
        [InlineKeyboardButton("Join Channel", url="https://t.me/movieshubmt")],
        [InlineKeyboardButton("Try Again", callback_data=text)]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def getMoviesListKeyboard(documents):
    keyboard = []

    for document in documents:
        logger.info(document)
        text = f"{document['size']} {document['caption']}"
        callback_data = f"{document['chat_id']}@@{document['message_id']}"
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
