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

def get_file_size(bytes):
    if bytes < 1024 ** 3:
        return f"{bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{bytes / (1024 ** 3):.2f} GB"

async def forward(from_, to_, files_channel, dump_channel):
    bot = telegram.Bot(token=BOT_TOKEN)

    count = 0
    for message_id in range(from_, to_+1):
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

            # message = await bot.forward_message(
            #     chat_id="-1001736615817",
            #     from_chat_id=BIN_CHANNEL,
            #     message_id=message_id
            # )

            # if message:
            #     save_message_to_db(message)
            #     await bot.delete_message(chat_id="-1001736615817", message_id=message.message_id)

            if message:
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
