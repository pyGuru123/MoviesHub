import json
from loguru import logger
import telegram

from app.pirates.utils import (
    isSubscriberOfMoviesHub,
    getJoinChannelKeyboard,
    sendKeyboard,
    copyFile,
    sendTextMessage,
    getMoviesListKeyboard
)

from app.pirates.database import (
    search_movie
)

async def main(request: dict):
    content = request["content"]
    logger.info(content)

    if "message" in content:
        chat_id = content["message"]["chat"]["id"]
        text = content["message"]["text"]
        reply_id = content["message"]["message_id"]
    elif "callback_query" in content:
        chat_id = content["callback_query"]["message"]["chat"]["id"]
        text = content["callback_query"]["data"]
        reply_id = content["callback_query"]["message"]["message_id"]

    isSubscriber = await isSubscriberOfMoviesHub(chat_id)
    if isSubscriber:
        logger.info(f"User is subscribed to the channel")

        if text.lower().strip() == "/start":
            await sendTextMessage(chat_id, "Send any movie name to search 🙂", reply_id)
        elif "@@" in text.strip():
            from_chat_id, message_id = map(int, text.split("@@"))
            await copyFile(chat_id, from_chat_id, message_id)
        else:
            documents = await search_movie(text.strip())
            if documents:
                reply_markup = await getMoviesListKeyboard(documents)
                await sendKeyboard(
                        chat_id=chat_id,
                        text=f"Found {len(documents)} movies",
                        reply_id=reply_id,
                        reply_markup=reply_markup
                    ) 
            else:
                await sendTextMessage(chat_id, "No Movie Found, try partial search 🙂", reply_id)
    else:
        logger.info(f"User is not subscribed to the channel")
        reply_markup = await getJoinChannelKeyboard(text)
        await sendKeyboard(
                chat_id=chat_id,
                text="Join our channel @movieshubmt to start using this bot",
                reply_id=reply_id,
                reply_markup=reply_markup
            )
        