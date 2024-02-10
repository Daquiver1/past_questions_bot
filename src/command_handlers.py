"""File contains all the handlers for the bot commands and messages."""

import time
from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from api_service import BackendClient
from config import BASE_URL
from helpers import ask_subscription_confirmation
from model import SubscriptionTier
from strings import Strings

command_handler_router = Router(name="CommandHandler")
api_service = BackendClient(BASE_URL)

strings = Strings()


@command_handler_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handles messages with the `/start` command."""
    try:
        registration_status = await check_or_register_user(message)
        if registration_status == "already_registered":
            await message.answer(
                strings.already_registered_message(message.from_user.full_name)
            )
        elif registration_status == "new_registration":
            await message.answer(strings.welcome_message(message.from_user.full_name))
        elif registration_status == "registration_failed":
            await message.answer(strings.failed_to_register_account_message())
    except Exception as e:
        print(f"Error in command_start_handler: {e}")
        await message.answer(strings.generic_error_message())


@command_handler_router.message(Command("subscription", ignore_case=True))
async def command_subscription_handler(message: Message) -> None:
    """Handles messages with the `/subscription` command."""
    try:
        await message.answer(strings.subscription_info_message())
    except Exception as e:
        print(f"Error in command_subscription_handler: {e}")
        await message.answer(strings.generic_error_message())


@command_handler_router.message(Command("subscribe", ignore_case=True))
async def command_subscribe_handler(message: types.Message) -> None:
    """Handles messages with the `/subscribe` command, allowing subscription to different tiers."""
    try:
        args = message.text.split()
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
            time.sleep(4)
            await message.answer(
                strings.completed_payment_question_message(), reply_markup=reply_markup
            )
        elif not response["success"] and response["status_code"] == 401:
            await message.answer(strings.unauthorized_user_message())
        else:
            await message.answer(strings.create_payment_failed_message())
    except Exception as e:
        print(f"Error in command_subscribe_handler: {e}")
        await message.answer(strings.generic_error_message())


async def check_or_register_user(message: Message) -> str:
    """Checks if a user is registered; if not, attempts to register them. Returns a string indicating the user's registration status ('already_registered', 'new_registration', or 'registration_failed')."""
    response = await api_service.get_user_details(message.from_user.id)
    if response["success"]:
        return "already_registered"
    else:
        response = await api_service.register_new_user(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
        if response["success"]:
            return "new_registration"
        else:
            return "registration_failed"
