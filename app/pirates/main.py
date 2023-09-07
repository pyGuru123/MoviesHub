import json
import telegram
from loguru import logger

from app.pirates.utils import (
    isSubscriberOfMoviesHub,
    getJoinChannelKeyboard,
    sendKeyboard,
    editKeyboard,
    copyFile,
    sendTextMessage,
    sendMarkupMessage
)

from app.pirates.functions import (
    get_libgen_links,
    get_ytsmx_links,
    get_piratesbay_links,
    get_bitsearch_links,
    get_magnetdl_links,
    get_nyaasi_links,
    get_zooqle_links
)


async def getChatInfo(content):
    chat_id, text, reply_id = None, None, None
    if "message" in content:
        chat_id = content["message"]["chat"]["id"]
        text = content["message"]["text"]
        reply_id = content["message"]["message_id"]
    elif "callback_query" in content:
        chat_id = content["callback_query"]["message"]["chat"]["id"]
        text = content["callback_query"]["data"]
        reply_id = content["callback_query"]["message"]["message_id"]

    return chat_id, text, reply_id


async def main(request: dict):
    content = request["content"]

    chat_id, text, reply_id = await getChatInfo(content)
    text = text.lower().strip()
    logger.info(f"{chat_id=} {text=} {reply_id=}")

    if text == "/start":
        await sendTextMessage(chat_id, "Send me a movie or a book name to find magnets 🙂", reply_id)
    elif text.startswith("/libgen"):
        query = " ".join(text.split()[1:])
        response = await get_libgen_links(query)
        await sendMarkupMessage(chat_id, response, reply_id)
    elif text.startswith("/ytsmx"):
        query = " ".join(text.split()[1:])
        response = await get_ytsmx_links(query)
        await sendMarkupMessage(chat_id, response, reply_id)
    elif text.startswith("/piratesbay"):
        query = " ".join(text.split()[1:])
        response = await get_piratesbay_links(query)
        await sendMarkupMessage(chat_id, response, reply_id)
    elif text.startswith("/bitsearch"):
        query = " ".join(text.split()[1:])
        response = await get_bitsearch_links(query)
        await sendMarkupMessage(chat_id, response, reply_id)
    elif text.startswith("/magnetdl"):
        query = " ".join(text.split()[1:])
        response = await get_magnetdl_links(query)
        await sendMarkupMessage(chat_id, response, reply_id)
    elif text.startswith("/nyaasi"):
        query = " ".join(text.split()[1:])
        response = await get_nyaasi_links(query)
        await sendMarkupMessage(chat_id, response, reply_id)
    elif text.startswith("/zooqle"):
        query = " ".join(text.split()[1:])
        response = await get_zooqle_links(query)
        await sendMarkupMessage(chat_id, response, reply_id)
            