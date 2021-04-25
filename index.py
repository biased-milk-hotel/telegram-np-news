import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Updater

from utils.database import check_if_exists, initialize, store
from utils.facebook import get_ronb

# configs
load_dotenv()
TOKEN = os.getenv('TOKEN')
db = "posts.db"


updater = Updater(
    token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
job = updater.job_queue


def send_notification(context):
    # context.bot.send_message(chat_id='@npnewsupdates',
    #                          text='One message every minute')
    if not os.path.isfile(db):
        logging.info("Database file not found; creating a new one...")
        initialize(db)

    ronb_posts = [x for x in get_ronb()].__reversed__()

    # TODO: add more here in future

    for post in ronb_posts:
        if not check_if_exists(db, post["post_id"]):
            print(f"Sending notification for {post['post_id']}")

            if post["image"]:
                context.bot.send_photo(
                    '@npnewsupdates', post["image"], caption=post["text"])
            else:
                context.bot.send_message(
                    '@npnewsupdates', text=post["text"])
            store(db, post)


if __name__ == "__main__":
    # main()
    telegram_job = job.run_repeating(send_notification, interval=60, first=10)

    updater.start_polling()
    updater.idle()
