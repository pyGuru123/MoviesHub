import os
import json
import platform
import requests
from math import ceil
from telegram import Bot
from telegram.constants import ParseMode
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

async def sendMarkupMessage(chat_id, text, reply_id):
    info = await pirates_bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_id,
                                        parse_mode=ParseMode.MARKDOWN)
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

