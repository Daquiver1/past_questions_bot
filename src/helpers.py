"""helpers.py"""

import re
from typing import Dict, List, Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from model import SubscriptionTier


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
        text="All",
        callback_data=f"question;all;{past_questions[0]['course_title']};{len(past_questions)}",
    )
    if not button_rows or len(button_rows[-1]) == row_limit:
        button_rows.append([all_button])
    else:
        button_rows[-1].append(all_button)

    return InlineKeyboardMarkup(inline_keyboard=button_rows)


def ask_subscription_confirmation(reference: str, plan: SubscriptionTier) -> InlineKeyboardMarkup:
    """Create a button layout asking the user to confirm subscription."""
    yes_button = InlineKeyboardButton(
        text="Yes, I've paid",
        callback_data=f"sub;{reference};{plan.tier_name};{plan.amount}",
    )

    keyboard = [[yes_button]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


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
