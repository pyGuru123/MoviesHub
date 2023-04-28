import time
import telegram
import asyncio
from app.model import Movie

BOT_TOKEN = os.getenv("BOT_TOKEN")
PUBLIC_CHANNEL = os.getenv("PUBLIC_CHANNEL")

async def forward(to_channel, limit, save_to_db=False):
    bot = telegram.Bot(token=BOT_TOKEN)

    for message_id in range(1):
        try:
            message = await bot.forward_message(
                chat_id=chat_id,
                from_chat_id=PUBLIC_CHANNEL,
                message_id=message_id
            )

            if save_to_db:
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

            await bot.delete_message(chat_id=chat_id, message_id=id_)
            time.sleep(1)
        except Exception as e:
            print(e)