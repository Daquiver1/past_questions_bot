"""Main file"""

import asyncio
import logging
import os
import sys

import dotenv
import sentry_sdk
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import ErrorEvent, Message, Update, URLInputFile
from aiogram.utils.markdown import hbold

from api_service import BackendClient
from filters import TextMatchFilter
from helpers import (
    ask_payment_confirmation,
    ask_subscription_confirmation,
    create_button_layout,
    create_filename_for_past_question,
    format_past_question_message,
    validate_user_input,
)
from model import SubscriptionTier
from strings import Strings

dotenv.load_dotenv()
TOKEN = os.environ["TOKEN"]
BASE_URL = os.environ["BASE_URL"]
ADMIN_TELEGRAM_ID = os.environ["ADMIN_TELEGRAM_ID"]
SENTRY_DSN_BOT = os.environ["SENTRY_DSN_BOT"]

dp = Dispatcher()
api_service = BackendClient(BASE_URL)
my_bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
strings = Strings()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handles messages with the `/start` command."""
    try:
        registration_status = await check_or_register_user(message)
        if registration_status == "already_registered":
            await message.answer(
                strings.already_registered_message(message.from_user.full_name)
            )
        elif registration_status == "new_registration":
            await message.answer(
                f"Hello, {hbold(strings.welcome_message(message.from_user.full_name))}!"
            )
        elif registration_status == "registration_failed":
            await message.answer(strings.failed_to_register_account_message())
    except Exception as e:
        print(f"Error in command_start_handler: {e}")
        await message.answer(strings.generic_error_message())


@dp.message(Command("subscription"))
async def command_subscription_handler(message: Message) -> None:
    """Handles messages with the `/subscription` command."""
    try:
        await message.answer(strings.subscription_info_message())
    except Exception as e:
        print(f"Error in command_subscription_handler: {e}")
        await message.answer(strings.generic_error_message())


@dp.message(Command("subscribe"))
async def command_subscribe_handler(message: types.Message) -> None:
    """Handles messages with the `/subscribe` command, allowing subscription to different tiers."""
    try:
        args = message.text.split()
        print(args)
        tier_arg = args[1] if len(args) > 1 else None

        if not tier_arg or tier_arg == "":
            await message.answer(strings.specify_subscription_tier_message())
            return
        tier = SubscriptionTier.from_arg(tier_arg)
        if not tier:
            await message.answer(strings.invalid_subscription_tier_message(tier_arg))
            return
        await message.answer(strings.subscribing_to_tier_message(tier.tier_name))
        response = await api_service.create_subscription_link(
            message.from_user.id, message.from_user.username, tier
        )
        if response["success"]:
            await message.answer(
                strings.make_payment_message(
                    response["data"]["authorization_url"], tier.tier_name
                )
            )
            reference = response["data"]["reference"]
            reply_markup = ask_subscription_confirmation(reference, tier)
            await message.answer(
                strings.completed_payment_question_message, reply_markup=reply_markup
            )
        else:
            await message.answer(strings.create_payment_failed_message())
    except Exception as e:
        print(f"Error in command_subscribe_handler: {e}")
        await message.answer(strings.generic_error_message())


@dp.message(TextMatchFilter("Daquiver"))
@dp.message(TextMatchFilter("Christian"))
async def handle_daquiver_message(message: types.Message) -> None:
    """Handles messages with the word "Daquiver"."""
    await message.answer(strings.daquiver_easter_egg_message())


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """Handler for all messages except commands."""
    try:
        user_input = message.text
        await message.answer(strings.echo_message(user_input))

        cleaned_input = validate_user_input(user_input)
        if not cleaned_input:
            await message.answer(strings.invalid_past_question_message())
            return

        await message.answer(strings.searching_past_question_message(cleaned_input))
        response = await api_service.get_past_questions(cleaned_input)
        if response["success"]:
            if not response["data"]:
                await message.answer(
                    strings.no_past_question_found_message(cleaned_input)
                )
                return
            await present_past_questions(
                message=message, past_questions=response["data"]
            )
        else:
            await message.answer(
                strings.failed_to_get_past_question_message(cleaned_input)
            )
    except TypeError as e:
        print(e)
        await message.answer(strings.invalid_type_message())
        print(e)
    except Exception as e:
        print(e)
        await message.answer(strings.generic_error_message())


@dp.callback_query(lambda c: c.data and c.data.startswith("sub"))
async def handle_subscription_confirmation(callback_query: types.CallbackQuery) -> None:
    """Handle button click."""
    _, reference, tier_name, amount = callback_query.data.split(";")
    await callback_query.answer()

    response = await api_service.verify_payment(reference)
    if response["success"] and response["data"]["data"]["status"] == "success":
        await callback_query.message.answer(strings.payment_successful_message())
        response = await api_service.create_subscription(
            callback_query.from_user.id, tier_name, amount, reference
        )
        if not response["success"]:
            await callback_query.message.answer(strings.failed_to_subscribe())
            # await send message to admin
            return
        await callback_query.message.answer(
            strings.subscription_successful_message(tier_name)
        )
    elif response["success"] and response["data"]["data"]["status"] == "abandoned":
        await callback_query.message.answer(strings.payment_not_started_message())
    elif response["success"] and response["data"]["data"]["status"] == "failed":
        await callback_query.message.answer(strings.payment_failed_message())
    else:
        await callback_query.message.answer(
            strings.payment_verification_failed_message()
        )


@dp.callback_query(lambda c: c.data and c.data.startswith("question"))
async def handle_question_selection(callback_query: types.CallbackQuery) -> None:
    """Handle button click."""
    _, index, past_question_id, length = callback_query.data.split(";")
    await callback_query.answer()

    response = await api_service.get_user_subscription(callback_query.from_user.id)
    if response and response["success"]:
        print(response["data"])
        balance, is_active = response["data"]["balance"], response["data"]["is_active"]
        balance, length = int(balance), int(length)
        if index == "all":
            if balance >= length and is_active:
                await callback_query.message.answer(strings.selected_all_message())
                await handle_all_questions(callback_query, past_question_id)
                await api_service.update_subscription_balance(
                    callback_query.from_user.id, int(balance) - int(length)
                )
                await callback_query.message.answer(
                    strings.update_past_question_number(length, balance)
                )
                return

            else:
                await callback_query.message.answer(
                    strings.not_enough_balance_message(balance, length)
                )
                return
        elif balance > 0 and is_active:
            await callback_query.message.answer(strings.selected_index_message(index))
            await handle_single_question(callback_query, past_question_id)
            await api_service.update_subscription_balance(
                callback_query.from_user.id, balance - 1
            )
            await callback_query.message.answer(
                strings.update_past_question_number(1, balance)
            )
            return

    payment_details = {
        "telegram_id": callback_query.from_user.id,
        "telegram_username": callback_query.from_user.username,
        "amount": length,
    }
    await callback_query.message.answer(strings.creating_payment_link())
    response = await api_service.create_payment_link(json=payment_details)
    if response["success"]:
        await callback_query.message.answer(
            strings.make_payment_message(response["data"]["authorization_url"])
        )
        reference = response["data"]["reference"]
        reply_markup = ask_payment_confirmation(index, past_question_id, reference)
        await callback_query.message.answer(
            strings.completed_payment_question_message(), reply_markup=reply_markup
        )
    else:
        await callback_query.message.answer(strings.create_payment_failed_message())
    return


@dp.callback_query(lambda c: c.data and not c.data.startswith("question"))
async def handle_payment_confirmation(callback_query: types.CallbackQuery) -> None:
    """Handle the user's response to the payment confirmation."""
    index, past_question_id, reference = callback_query.data.split(";")
    await callback_query.answer()

    response = await api_service.verify_payment(reference)
    if response["success"] and response["data"]["data"]["status"] == "success":
        await callback_query.message.answer(strings.payment_successful_message())

        if index == "all":
            await callback_query.message.answer(strings.selected_all_message())
            await handle_all_questions(callback_query, past_question_id)
        else:
            await callback_query.message.answer(strings.selected_index_message(index))
            await handle_single_question(callback_query, past_question_id)
    elif response["success"] and response["data"]["data"]["status"] == "abandoned":
        await callback_query.message.answer(strings.payment_not_started_message())
    elif response["success"] and response["data"]["data"]["status"] == "failed":
        await callback_query.message.answer(strings.payment_failed_message())
    else:
        await callback_query.message.answer(
            strings.payment_verification_failed_message()
        )


@dp.error()
async def error_handler(event: ErrorEvent) -> None:
    """Global error handler. Logs the error and sends it to the admin."""
    await send_error_to_user(event.exception, event.update)
    await send_error_to_admin(event.exception, event.update)


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
        strings.found_past_question_message(
            len(past_questions), past_questions[0]["course_title"]
        )
    )

    message_text = strings.past_questions_title_message(
        past_questions[0]["course_title"]
    )
    message_lines = [
        format_past_question_message(index, question)
        for index, question in enumerate(past_questions, start=1)
    ]
    message_text = "\n".join(message_lines)

    reply_markup = create_button_layout(past_questions)

    await message.answer(message_text)
    await message.answer(
        strings.past_question_to_download_message, reply_markup=reply_markup
    )


async def handle_all_questions(
    callback_query: types.CallbackQuery, past_question_id: str
) -> None:
    """Handle all questions"""
    response = await api_service.get_past_questions(past_question_id)
    if response.get("success"):
        await callback_query.message.answer(
            strings.sending_all_past_questions_message()
        )
        for past_question in response["data"]:
            await send_past_question(callback_query, past_question)
        await callback_query.message.answer(strings.done_message())
    else:
        await callback_query.message.answer(
            strings.failed_to_get_past_question_message()
        )


async def handle_single_question(
    callback_query: types.CallbackQuery, past_question_id: str
) -> None:
    """Handle single question"""
    response = await api_service.get_past_question(past_question_id)
    if response.get("success"):
        await callback_query.message.answer(strings.sending_past_question_message())
        await send_past_question(callback_query, response["data"])
        await callback_query.message.answer(strings.done_message())

    else:
        await callback_query.message.answer(
            strings.failed_to_get_past_question_message()
        )


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
    if update and update.message:
        user_id = update.message.from_user.id
        username = update.message.from_user.username
        message_text = update.message.text
    elif update and update.callback_query:
        user_id = update.callback_query.from_user.id
        username = update.callback_query.from_user.username
        message_text = update.callback_query.data

    error_message = strings.format_error_message_to_admin(
        exception, user_id, username, message_text
    )
    await my_bot.send_message(chat_id=ADMIN_TELEGRAM_ID, text=error_message)


async def main() -> None:
    """Main function"""
    await dp.start_polling(my_bot)


if __name__ == "__main__":
    sentry_sdk.init(
        dsn=SENTRY_DSN_BOT,
        environment="development",
        traces_sample_rate=0.0001,
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        stream=sys.stdout,
    )
    asyncio.run(main())
