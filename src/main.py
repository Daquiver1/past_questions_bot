"""Main file"""
import asyncio
import logging
import sys
import os
import sentry_sdk
import dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, URLInputFile, ErrorEvent
from aiogram.utils.markdown import hbold

from api_service import BackendClient
from helpers import (
    welcome_message,
    validate_user_input,
    invalid_past_question_message,
    searching_past_question_message,
    failed_to_register_account_message,
    generic_error_message,
    create_button_layout,
    already_registered_message,
    format_past_question_message,
    create_filename_for_past_question,
    format_error_message_to_admin,
)

dotenv.load_dotenv()
TOKEN = os.environ["TOKEN"]
BASE_URL = os.environ["BASE_URL"]
ADMIN_TELEGRAM_ID = os.environ["ADMIN_TELEGRAM_ID"]
SENTRY_DSN_BOT = os.environ["SENTRY_DSN_BOT"]

dp = Dispatcher()
api_service = BackendClient(BASE_URL)
my_bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handles messages with the `/start` command."""
    try:
        registration_status = await check_or_register_user(message)
        if registration_status == "already_registered":
            await message.answer(
                already_registered_message(message.from_user.full_name)
            )
        elif registration_status == "new_registration":
            await message.answer(
                f"Hello, {hbold(welcome_message(message.from_user.full_name))}!"
            )
        elif registration_status == "registration_failed":
            await message.answer(failed_to_register_account_message())
    except Exception as e:
        print(f"Error in command_start_handler: {e}")
        await message.answer(generic_error_message())


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """Handler for all messages except commands."""
    try:
        user_input = message.text
        await message.answer(f"You said {user_input}")

        cleaned_input = validate_user_input(user_input)
        if not cleaned_input:
            await message.answer(
                f"{hbold('Invalid past question name')}\n\n{invalid_past_question_message()}"
            )
            return

        await message.answer(searching_past_question_message(cleaned_input))
        response = await api_service.get_past_questions(cleaned_input)
        if response["success"]:
            if not response["data"]:
                await message.answer(f"No {cleaned_input} past question found")
                return
            await present_past_questions(
                message=message, past_questions=response["data"]
            )
        else:
            await message.answer("Failed to get past question")
    except TypeError as e:
        await message.answer("Invalid type")
        print(e)
    except Exception as e:
        print(e)
        await message.answer(generic_error_message())


@dp.callback_query()
async def handle_button(callback_query: types.CallbackQuery) -> None:
    """Handle button click."""
    index, past_question_id = callback_query.data.split(";")
    await callback_query.answer()

    if index == "all":
        await callback_query.message.answer("You selected all")
        await handle_all_questions(callback_query, past_question_id)
    else:
        await callback_query.message.answer(f"You selected #{index}")
        await handle_single_question(callback_query, past_question_id)


@dp.error()
async def error_handler(event: ErrorEvent) -> None:
    """Global error handler. Logs the error and sends it to the admin."""
    await send_error_to_admin(event.exception, event.update.message)


async def check_or_register_user(message: Message) -> str:
    """Checks if a user is registered; if not, attempts to register them. Returns a string indicating the user's registration status ('already_registered', 'new_registration', or 'registration_failed')."""
    response = await api_service.get_user_details(message.from_user.id)
    if response["success"]:
        return "already_registered"

    user_details = {
        "telegram_id": message.from_user.id,
        "username": message.from_user.username or "",
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name or "",
    }
    response = await api_service.register_new_user(json=user_details)
    if response["success"]:
        return "new_registration"
    else:
        return "registration_failed"


async def present_past_questions(message: types.Message, past_questions: list) -> None:
    """Present past questions to user"""
    await message.answer(
        f"We found {len(past_questions)} {past_questions[0]['course_title']} past questions"
    )

    message_text = f"{past_questions[0]['course_title']} Questions:\n\n"
    message_lines = [
        format_past_question_message(index, question)
        for index, question in enumerate(past_questions, start=1)
    ]
    message_text = "\n".join(message_lines)

    reply_markup = create_button_layout(past_questions)

    await message.answer(message_text)
    await message.answer(
        "Which one do you want to download?", reply_markup=reply_markup
    )


async def handle_all_questions(
    callback_query: types.CallbackQuery, past_question_id: str
) -> None:
    """Handle all questions"""
    print(past_question_id)
    response = await api_service.get_past_questions(past_question_id)
    if response.get("success"):
        await callback_query.message.answer("Sending all past questions...")
        for past_question in response["data"]:
            await send_past_question(callback_query, past_question)
        await callback_query.message.answer("Done!")
    else:
        await callback_query.message.answer("Failed to get past questions.")


async def handle_single_question(
    callback_query: types.CallbackQuery, past_question_id: str
) -> None:
    """Handle single question"""
    response = await api_service.get_past_question(past_question_id)
    if response.get("success"):
        await callback_query.message.answer("Sending past question...")
        await send_past_question(callback_query, response["data"])
    else:
        await callback_query.message.answer("Failed to get past question.")


async def send_past_question(
    callback_query: types.CallbackQuery, past_question: dict
) -> None:
    """Send past question to user"""
    document = URLInputFile(
        past_question["past_question_url"],
        filename=create_filename_for_past_question(past_question),
    )
    await callback_query.message.answer_document(document=document)
    await api_service.create_download(callback_query.from_user.id, past_question["id"])


async def send_error_to_admin(exception: Exception, message: Message) -> None:
    """Sends an error message to the admin Telegram ID with details about the exception."""
    error_message = format_error_message_to_admin(
        exception, message.from_user, message.text
    )
    await my_bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text=error_message)


async def main() -> None:
    """Main function"""
    await dp.start_polling(my_bot)


if __name__ == "__main__":
    sentry_sdk.init(
        dsn=SENTRY_DSN_BOT,
        environment="development",
        traces_sample_rate=0.1,
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    asyncio.run(main())
