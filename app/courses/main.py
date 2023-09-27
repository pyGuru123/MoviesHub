import json
import telegram
from loguru import logger

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
        logger.info("bot started")