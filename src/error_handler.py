"""Contains functions to handle errors and send error messages to the user and admin."""

from aiogram import Bot, Router
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent, Update

from config import ADMIN_TELEGRAM_ID, TOKEN
from strings import Strings

my_bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
strings = Strings()
error_handler_router = Router(name="ErrorHandler")


@error_handler_router.error()
async def error_handler(event: ErrorEvent) -> None:
    """Global error handler. Logs the error and sends it to the admin."""
    await send_error_to_user(event.exception, event.update)
    await send_error_to_admin(event.exception, event.update)


async def send_error_to_user(exception: Exception, update: Update) -> None:
    """Sends an error message to the user with details about the exception."""
    user_id = None
    if update and update.message:
        user_id = update.message.from_user.id
    elif update and update.callback_query:
        user_id = update.callback_query.from_user.id

    await my_bot.send_message(
        chat_id=user_id, text=strings.error_message_to_user_message()
    )


async def send_error_to_admin(exception: Exception, update: Update) -> None:
    """Sends an error message to the admin Telegram ID with details about the exception."""
    user_id = None
    username = "Unknown"
    message_text = None
    if update and update.callback_query:
        user_id = update.callback_query.from_user.id
        username = update.callback_query.from_user.username
        message_text = update.callback_query.data
    elif update and update.message:
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        message_text = update.message.text

    error_message = strings.format_error_message_to_admin(
        exception, user_id, username, message_text
    )
    await my_bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text=error_message)
