import os
import time
import telegram
import asyncio
from app.model import Movie

BOT_TOKEN = os.getenv("BOT_TOKEN")
BIN_CHANNEL = os.getenv("BIN_CHANNEL")
FILES_CHANNEL = os.getenv("FILES_CHANNEL")
DUMP_CHANNEL = os.getenv("DUMP_CHANNEL")

CHANNELS = [FILES_CHANNEL, DUMP_CHANNEL]

async def forward(from_, to_, files_channel, dump_channel):
    bot = telegram.Bot(token=BOT_TOKEN)
    print(to_, from_, files_channel, dump_channel)

    count = 0
    for message_id in range(from_, to_+1):
        print(message_id)
        try:
            if files_channel:
                message = await bot.copy_message(
                    chat_id=FILES_CHANNEL,
                    from_chat_id=BIN_CHANNEL,
                    message_id=message_id
                )

            if dump_channel:
                message = await bot.copy_message(
                    chat_id=DUMP_CHANNEL,
                    from_chat_id=BIN_CHANNEL,
                    message_id=message_id
                )

            count += 1
                
            time.sleep(1)
        except Exception as e:
            print(e)

    return count

def save_message_to_db(message):
    img_url = ""
    caption = message.caption
    id_ = message.message_id
    text480p, url480p, text720p, url720p, text1080p, url1080p = "", "", "", "", "", ""
    rows = message.reply_markup.inline_keyboard
    for row in rows:
        for button in row:
            if "480" in button.text: 
                text480p, url480p = button.text, button.url
            if "720" in button.text: 
                text720p, url720p = button.text, button.url
            if "1080" in button.text: 
                text1080p, url1080p = button.text, button.url

    print(caption)
    movie = Movie(
        img_url=img_url,
        caption=caption,
        text480p=text480p,
        url480p=url480p,
        text720p=text720p,
        url720p=url720p,
        text1080p=text1080p,
        url1080p=url1080p)

    movie.save()

    # await bot.delete_message(chat_id=chat_id, message_id=id_)