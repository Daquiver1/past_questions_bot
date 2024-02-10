"""File contains all the handlers for the bot callback queries."""

import time

from aiogram import Router, types
from aiogram.types import URLInputFile

from api_service import BackendClient
from config import BASE_URL
from error_handler import send_error_to_admin
from helpers import ask_payment_confirmation, create_filename_for_past_question
from strings import Strings

callback_query_handler = Router(name="CallbackQueryHandler")
api_service = BackendClient(BASE_URL)

strings = Strings()


@callback_query_handler.callback_query(lambda c: c.data and c.data.startswith("sub"))
async def handle_subscription_confirmation(callback_query: types.CallbackQuery) -> None:
    """Handle button click."""
    _, reference, tier_name, amount = callback_query.data.split(";")
    await callback_query.answer()

    print(reference, tier_name, amount)
    response = await api_service.verify_payment(callback_query.from_user.id, reference)

    if response["success"] and response["data"]["data"]["status"] == "success":
        await callback_query.message.answer(strings.payment_successful_message())
        response = await api_service.create_subscription(
            callback_query.from_user.id, tier_name, amount, reference
        )
        if not response["success"] and response["status_code"] == 401:
            await callback_query.message.answer(strings.unauthorized_user_message())
            return
        elif not response["success"]:
            await callback_query.message.answer(strings.failed_to_subscribe())
            await send_error_to_admin(
                Exception("User failed to subscribe after paying."), callback_query
            )
            return
        await callback_query.message.answer(
            strings.subscription_successful_message(tier_name)
        )
    elif response["success"] and response["data"]["data"]["status"] == "abandoned":
        await callback_query.message.answer(strings.payment_not_started_message())
    elif response["success"] and response["data"]["data"]["status"] == "failed":
        await callback_query.message.answer(strings.payment_failed_message())
    elif not response["success"] and response["status_code"] == 401:
        await callback_query.message.answer(strings.unauthorized_user_message())
    else:
        await callback_query.message.answer(
            strings.payment_verification_failed_message()
        )


@callback_query_handler.callback_query(
    lambda c: c.data and c.data.startswith("question")
)
async def handle_question_selection(callback_query: types.CallbackQuery) -> None:
    """Handle button click."""
    _, index, past_question_id, length = callback_query.data.split(";")
    await callback_query.answer()

    response = await api_service.get_user_subscription(callback_query.from_user.id)
    if response and response["success"]:
        balance, is_active = response["data"]["balance"], response["data"]["is_active"]
        balance, length = int(balance), int(length)
        if index == "all":
            if balance >= length and is_active:
                await callback_query.message.answer(strings.selected_all_message())
                await handle_all_questions(callback_query, past_question_id)
                response = await api_service.update_subscription_balance(
                    callback_query.from_user.id, int(balance) - int(length)
                )
                if not response["success"] and response["status_code"] == 401:
                    await callback_query.message.answer(
                        strings.unauthorized_user_message()
                    )
                    return
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
            response = await api_service.update_subscription_balance(
                callback_query.from_user.id, balance - 1
            )
            if not response["success"] and response["status_code"] == 401:
                await callback_query.message.answer(strings.unauthorized_user_message())
                return
            await callback_query.message.answer(
                strings.update_past_question_number(1, balance)
            )
            return
    elif not response["success"] and response["status_code"] == 401:
        await callback_query.message.answer(strings.unauthorized_user_message())
        return
    await callback_query.message.answer(strings.no_active_subscription_message())
    await callback_query.message.answer(strings.creating_payment_link())
    response = await api_service.create_payment_link(
        callback_query.from_user.id, callback_query.from_user.username, length
    )
    if response["success"]:
        await callback_query.message.answer(
            strings.make_payment_message(response["data"]["authorization_url"])
        )
        reference = response["data"]["reference"]
        reply_markup = ask_payment_confirmation(index, past_question_id, reference)
        time.sleep(4)
        await callback_query.message.answer(
            strings.completed_payment_question_message(), reply_markup=reply_markup
        )
    elif not response["success"] and response["status_code"] == 401:
        await callback_query.message.answer(strings.unauthorized_user_message())
    else:
        await callback_query.message.answer(strings.create_payment_failed_message())
    return


@callback_query_handler.callback_query(
    lambda c: c.data and not c.data.startswith("question")
)
async def handle_payment_confirmation(callback_query: types.CallbackQuery) -> None:
    """Handle the user's response to the payment confirmation."""
    index, past_question_id, reference = callback_query.data.split(";")
    await callback_query.answer()

    response = await api_service.verify_payment(callback_query.from_user.id, reference)
    if response["success"] and response["data"]["data"]["status"] == "success":
        await callback_query.message.answer(strings.payment_successful_message())

        if index == "all":
            await callback_query.message.answer(strings.selected_all_message())
            await handle_all_questions(callback_query, past_question_id)
            await callback_query.message.answer(strings.can_create_subscription_message())
        else:
            await callback_query.message.answer(strings.selected_index_message(index))
            await handle_single_question(callback_query, past_question_id)
    elif response["success"] and response["data"]["data"]["status"] == "abandoned":
        await callback_query.message.answer(strings.payment_not_started_message())
    elif response["success"] and response["data"]["data"]["status"] == "failed":
        await callback_query.message.answer(strings.payment_failed_message())
    elif not response["success"] and response["status_code"] == 401:
        await callback_query.message.answer(strings.unauthorized_user_message())
    else:
        await callback_query.message.answer(
            strings.payment_verification_failed_message()
        )


async def handle_all_questions(
    callback_query: types.CallbackQuery, past_question_id: str
) -> None:
    """Handle all questions"""
    response = await api_service.get_past_questions(
        callback_query.from_user.id, past_question_id
    )
    if response["success"]:
        await callback_query.message.answer(
            strings.sending_all_past_questions_message()
        )
        for past_question in response["data"]:
            await send_past_question(callback_query, past_question)
        await callback_query.message.answer(strings.done_message())
    elif not response["success"] and response["status_code"] == 401:
        await callback_query.message.answer(strings.unauthorized_user_message())
    else:
        await callback_query.message.answer(
            strings.failed_to_get_past_question_message()
        )


async def handle_single_question(
    callback_query: types.CallbackQuery, past_question_id: str
) -> None:
    """Handle single question"""
    response = await api_service.get_past_question(
        callback_query.from_user.id, past_question_id
    )
    if response["success"]:
        await callback_query.message.answer(strings.sending_past_question_message())
        await send_past_question(callback_query, response["data"])
        await callback_query.message.answer(strings.done_message())
    elif not response["success"] and response["status_code"] == 401:
        await callback_query.message.answer(strings.unauthorized_user_message())
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
