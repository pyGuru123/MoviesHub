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
    getMoviesListKeyboard
)

from app.pirates.database import (
    search_movie
)

from app.pirates.session import *


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
    if chat_id and not str(chat_id).startswith("-"):
        isSubscriber = await isSubscriberOfMoviesHub(chat_id)
        if isSubscriber:
            if text.lower().strip() == "/start":
                await sendTextMessage(chat_id, "Send any movie name to search 🙂", reply_id)
            elif "@@" in text.strip():
                from_chat_id, message_id = map(int, text.split("@@"))
                await copyFile(chat_id, from_chat_id, message_id)
            elif text.startswith("@"):
                pass
            elif text == "next:next":
                session_token = f"user:{chat_id}"
                data = get_user_from_session(session_token)
                if data:
                    documents, page, reply_id = data
                    reply_markup, page = await getMoviesListKeyboard(documents, page, "next")
                    if reply_markup:
                        response = await editKeyboard(
                                chat_id=chat_id,
                                text=f"Found {len(documents)} files",
                                reply_id=reply_id,
                                reply_markup=reply_markup
                            )

                        session_token = update_session(str(chat_id), page)
                else:
                   await sendTextMessage(str(chat_id), "Session Expired", reply_id)
            elif text == "prev:prev":
                session_token = f"user:{chat_id}"
                data = get_user_from_session(session_token)
                if data:
                    documents, page, reply_id = data
                    reply_markup, page = await getMoviesListKeyboard(documents, page, "prev")
                    if reply_markup:
                        response = await editKeyboard(
                                chat_id=chat_id,
                                text=f"Found {len(documents)} files",
                                reply_id=reply_id,
                                reply_markup=reply_markup
                            )

                        session_token = update_session(str(chat_id), page)
                else:
                   await sendTextMessage(str(chat_id), "Session Expired", reply_id)
            else:
                if text != "status":
                    documents = await search_movie(text.strip())
                    if documents:
                        reply_markup, page = await getMoviesListKeyboard(documents)
                        response = await sendKeyboard(
                                chat_id=chat_id,
                                text=f"Found {len(documents)} files",
                                reply_id=reply_id,
                                reply_markup=reply_markup
                            )
                        session_token = create_session(str(chat_id), response.message_id, documents, page)
                    else:
                        await sendTextMessage(chat_id, "No Movie Found, try partial search 🙂", reply_id)
        else:
            reply_markup = await getJoinChannelKeyboard(text)
            await sendKeyboard(
                    chat_id=chat_id,
                    text="Join our channel @movieshubmt to start using this bot",
                    reply_id=reply_id,
                    reply_markup=reply_markup
                )
            