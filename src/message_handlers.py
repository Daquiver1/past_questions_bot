"""Contains message handlers for the bot."""

from aiogram import Router, types
from aiogram.filters.command import Command

from api_service import BackendClient
from config import BASE_URL
from filters import TextMatchFilter
from helpers import (
    create_button_layout,
    format_past_question_message,
    validate_user_input,
)
from strings import Strings

api_service = BackendClient(BASE_URL)
strings = Strings()

message_handler_router = Router(name="MessageHandler")


@message_handler_router.message(TextMatchFilter("Daquiver"))
@message_handler_router.message(TextMatchFilter("Christian"))
async def handle_daquiver_message(message: types.Message) -> None:
    """Handles messages with the word "Daquiver"."""
    await message.answer(strings.daquiver_easter_egg_message())


@message_handler_router.message(
    ~Command(commands=["start", "subscription", "subscribe"], ignore_case=True)
)
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
        response = await api_service.get_past_questions(
            message.from_user.id, cleaned_input
        )
        if response["success"]:
            if not response["data"]:
                await message.answer(
                    strings.no_past_question_found_message(cleaned_input)
                )
                return
            await present_past_questions(
                message=message, past_questions=response["data"]
            )
        elif not response["success"] and response["status_code"] == 401:
            await message.answer(strings.unauthorized_user_message())
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
        strings.past_question_to_download_message(), reply_markup=reply_markup
    )
