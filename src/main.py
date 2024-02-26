"""Main bot file."""

import logging
import logging.config
import os

import dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Logging setup
logging.config.fileConfig(
    fname="log.ini",
    disable_existing_loggers=False,
)

logger = logging.getLogger(__name__)

dotenv.load_dotenv()
PORT = int(os.environ.get("PORT", "8443"))
TOKEN = os.environ["TOKEN"]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle message."""
    text = (
        f"Hello {update.message.from_user.username}\n\n"
        "Due to the high number of errors, this bot has been deprecated and will be archived on June 1st 2024.\n\n"
        "For the new and improved bot, please visit @QuiverTech_pasco_bot\n\n"
        "Thank you!"
    )
    await update.message.reply_text(text)


def main():
    """Start bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # for polling
    app.run_polling()

    # app.run_webhook(
    #     listen="0.0.0.0",
    #     port=PORT,
    #     url_path=TOKEN,
    #     webhook_url="https://past-questions-bot.herokuapp.com/" + TOKEN,
    # )


if __name__ == "__main__":
    main()
