from dotenv import load_dotenv, find_dotenv
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

from functions import start, handle_message, error_handler

load_dotenv(find_dotenv())

TOKEN = os.environ.get('TOKEN')


def main():
    """Setup bot"""
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (filters.COMMAND), handle_message))
    app.add_error_handler(error_handler)

    print('Setup completed')

    app.run_polling()


if __name__ == '__main__':
    main()