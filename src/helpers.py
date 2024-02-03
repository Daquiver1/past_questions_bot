"""helpers.py"""
import re
from typing import Dict, Optional, List
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime


def welcome_message(username: str) -> str:
    """Welcome message."""
    return f"""{username},
Welcome to Daquiver's Past Questions bot

Type the name of the past question, select the one you want and it'll be sent to you.
Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 )
Check the /about section for more info.
"""


def invalid_past_question_message() -> str:
    """Invalid past question message."""
    return """Please enter a valid past question name. Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 )"""


def searching_past_question_message(past_question_name: str) -> str:
    """Searching past question message."""
    return f"""Searching for {past_question_name} past questions..."""


def already_registered_message(past_question_name: str) -> str:
    """Already registered message."""
    return f"""Hello, {past_question_name},
You account has already been registered!

To request a past question please type the past questions course name and course code.
Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 )."""


def failed_to_register_account_message() -> str:
    """Failed to register account message."""
    return """Failed to register your account, please try again later."""


def generic_error_message() -> str:
    """Generic error message."""
    return """Sorry, there was a problem processing your request."""


def format_error_message_to_admin(
    exception: Exception, user_id: str, username: str, last_message: str
) -> str:
    """Format error message to admin."""
    error_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # traceback_details = "".join(traceback.format_exception(exception))

    error_message = f"""Error occurred:
Timestamp: {error_timestamp}
User ID: {user_id}
Username: @{username}
Last Message: {last_message or 'N/A'}

The type of error: {type(exception).__name__}
The error message: {str(exception)}
"""
    return error_message


def create_filename_for_past_question(past_question: dict) -> str:
    """Create filename for past question."""
    course_title = past_question.get("course_title", "PastQuestion")
    semester = past_question.get("semester", "")
    year = past_question.get("year", "")

    filename = f"{course_title}_{semester}_{year}.pdf"
    filename = filename.replace("/", "_").replace("\\", "_").replace(":", "_")

    return filename


def format_past_question_message(index: int, past_question: Dict) -> str:
    """Display past question display message."""
    return f"""{index}. {past_question['course_title'].upper()}: {past_question['course_name'].upper()}, Examination Year: {past_question['year']}, Semester: {past_question['semester']}\n"""


def create_button_layout(
    past_questions: List[dict], row_limit: int = 7
) -> InlineKeyboardMarkup:
    """Create button layout for past questions."""
    button_rows: List[List[InlineKeyboardButton]] = []
    current_row = []

    for i, question in enumerate(past_questions, start=1):
        button_text = str(i)
        callback_data = f"question;{i};{question['id']};1"
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)

        current_row.append(button)
        if len(current_row) == row_limit or i == len(past_questions):
            button_rows.append(current_row)
            current_row = []

    all_button = InlineKeyboardButton(
        text="All", callback_data=f"question;all;{past_questions[0]['course_title']};{len(past_questions)}"
    )
    if not button_rows or len(button_rows[-1]) == row_limit:
        button_rows.append([all_button])
    else:
        button_rows[-1].append(all_button)

    return InlineKeyboardMarkup(inline_keyboard=button_rows)


def ask_payment_confirmation(
    index: int, past_question_id: str, reference: str
) -> InlineKeyboardMarkup:
    """Create a button layout asking the user if they've paid."""
    yes_button = InlineKeyboardButton(
        text="Yes, I've paid",
        callback_data=f"{index};{past_question_id};{reference}",
    )

    keyboard = [[yes_button]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def validate_user_input(past_question_name: str) -> Optional[str]:
    """Check if string is a valid past question name"""
    past_question_name = past_question_name.strip().lower()
    numbers_text_check = re.compile("^([a-zA-Z]{4})([0-9]{3})$")
    result = numbers_text_check.match(past_question_name.replace(" ", ""))

    if result:
        course_name, course_code = result.groups()
        return f"{course_name} {course_code}"
    return None
