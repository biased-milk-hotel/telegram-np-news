import logging
import os
import re

import tweepy
from dotenv import load_dotenv
from telegram import (InputMediaPhoto, ParseMode)
from telegram.ext import Updater

from keep_alive import keep_alive
from utils.database import check_if_exists, initialize, store
from utils.twitter import get_ronb

keep_alive()

# configs
# -----------------------------------------------------

load_dotenv()
# Telegram
TOKEN = os.getenv('TOKEN')
CHANNEL = os.getenv('CHANNEL')

# Twitter
TWITTER_API = os.getenv('TWITTER_API')
TWITTER_SECRET = os.getenv('TWITTER_SECRET')

DB = "posts.db"
# -----------------------------------------------------


# tweepy setup
auth = tweepy.AppAuthHandler(TWITTER_API, TWITTER_SECRET)
api = tweepy.API(auth)

updater = Updater(
    token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
job = updater.job_queue


def send_notification(context):
    if not os.path.isfile(DB):
        logging.info("Database file not found; creating a new one...")
        initialize(DB)
    print("Fetching contents...")
    ronb_posts = [x for x in get_ronb(api)].__reversed__()
    for post in ronb_posts:
        source_text = f"\n\n[<a href=\"{post['post_url']}\">Source</a>]"
        if not check_if_exists(DB, post["post_id"]):
            print(f"Sending notification for {post['post_id']}")
            if post["images"]:
                telegram_media = [InputMediaPhoto(
                    media=x,
                    caption=re.sub(r"(http|https)://t\.\S+", "",
                                   post["text"]) + source_text,
                    parse_mode=ParseMode.HTML,
                ) for x in post["images"]]

                context.bot.send_media_group(
                    CHANNEL,
                    media=telegram_media,)
        else:
            context.bot.send_message(
                CHANNEL,
                text=post["text"] + source_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True)
        store(DB, post)


if __name__ == "__main__":
    telegram_job = job.run_repeating(send_notification, interval=600, first=10)

    updater.start_polling()
    updater.idle()
