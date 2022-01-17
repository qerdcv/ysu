import os
import logging
import re

import requests
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

EMBEDED_URL_RE = re.compile(r'rel="shortlinkUrl" href="(.+?)">')
SHORTS_REGEX = re.compile(r'https://(www\.)?youtube.com/shorts/')
RESP = """FROM: @{}
{}
"""

bot = Bot(token=os.environ['TG_BOT_TOKEN'])
dp = Dispatcher(bot)


@dp.message_handler()
async def handle_message(message: types.Message):
    if SHORTS_REGEX.match(message.text):
        resp = requests.get(message.text)  # TODO: use async client
        if not resp.ok:
            await bot.send_message(
                message.chat.id,
                f"Failed to get video cause of {resp.text}"
            )
            return
        await bot.send_message(
            message.chat.id,
            RESP.format(message.from_user.username, EMBEDED_URL_RE.search(resp.text).group(1))
        )
        await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
