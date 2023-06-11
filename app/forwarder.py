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

            save_message_to_db(message)
            count += 1
                
            time.sleep(1)
        except Exception as e:
            print(e)

    return count

def save_message_to_db(message):
    video = False

    if message.video:
        caption = message.caption or message.video.file_name
        size = get_file_size(message.video.file_size)
        channel_id = message.forward_from_chat.id
        msg_id = message.forward_from_message_id
        unique_id = message.video.file_unique_id
        video = True

    elif message.document:
        caption = message.caption or message.document.file_name
        size = get_file_size(message.document.file_size)
        channel_id = message.forward_from_chat.id
        msg_id = message.forward_from_message_id
        unique_id = message.document.file_unique_id
        video = True


    if video:
        movie = Movie(caption, size, channel_id, msg_id, unique_id)
        movie.save()
