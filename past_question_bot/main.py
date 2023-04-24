"""Main bot file."""
import logging
import logging.config
import os
import re
import sys
import traceback
from typing import List, Union

import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          ContextTypes, MessageHandler, filters)

from past_question_bot.helpers import Scrapper

from past_question_bot.constant import (APPLICATIONS, DEVELOPER_CHAT_ID, ENV,
                                        PORT, TOKEN)

logger = logging.getLogger("past_question_bot")

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command."""
    await update.message.reply_text(
        f"""
    Hello {update.message.from_user.username}
Welcome to Daquiver's Past Questions bot

Type the name of the past question, select the one you want and it'll be sent to you.
Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 )
Check the /about section for more info.

        """
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command."""
    await update.message.reply_text(
        """
    The following commands are available:

/donate -> Buy me a drink.
/start -> Welcome Message.
/help -> This Message.
/contact -> My contact details.
/about -> Why did I build this?
    """
    )


async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Donate command."""
    await update.message.reply_text(
        "Thanks for buying me coffee. Details below.\nName: Christian Abrokwa\nNumber: 0547642843"
    )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contact command."""
    await update.message.reply_text(
        """
        You can contact me via the following:
Gmail: Cabrokwa11@gmail.com

Telegram: @Daquiver

Github: https://github.com/Daquiver1

Twitter: https://www.twitter.com/daquiver1

LinkedIn: https://www.linkedin.com/in/daquiver
        """
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About command."""
    await update.message.reply_text(
        """
    Hey I'm Christian, Christian Abrokwa. Nice to meet you.

During the day I'm a software engineer and at nights I'm a superhero. Somewhere in between, I perform my student responsibilities. \nSo why did I build this?

I noticed there was a bottleneck with the current system of getting a past question. It took a student about a week to get access to a past question. So, I built and developed this system which allows University of Ghana students to download past questions under 30 seconds.

It works by scraping the ug past questions site(https://balme.ug.edu.gh/past.exampapers/index.php) and returning files matching the users criteria.

It can only download past questions on the ug site. So if a past question isn't found, it means the University haven't uploaded the past question.

* This bot was built on January 4th, 2022.
        """
    )


async def get_chat_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, str]:
    """
    It returns the chat id of the message that triggered the bot

    Args:
      update (Update): Update
      context (ContextTypes.DEFAULT_TYPE): ContextTypes.DEFAULT_TYPE

    Returns:
      The chat id of the user who sent the message.
    """
    # text message
    if update.message is not None:
        return update.message.chat.id
    # callback message
    elif update.callback_query is not None:
        return update.callback_query.message.chat.id
    return -1


def validate_user_input(past_question_name: str) -> Union[str, None]:
    """
    It takes a string, checks if it's a valid course name and code, and returns the cleaned string if it is. A cleaned string is one which has a space in between the course name and course code. The website's search field won't work if it isn't spaced.

    Args:
      past_question_name (str): str

    Returns:
      a string or None.
    """
    if len(past_question_name.split()) == 1:
        numbers_text_check = re.compile(
            "([a-zA-Z]+)([0-9]+)"
        )  # Check for numbers and text combined(no space)
        result = numbers_text_check.match(past_question_name)
        if result:
            result = result.groups()
        return None
    else:
        result = past_question_name.split()

    course_name = result[0]  # Course name
    course_code = result[-1]  # Course code

    if course_name.isalpha() is False:
        return None

    if len(course_name) != 4:  # Legon course names have 4 characters.
        return None

    if course_code.isnumeric() is False:
        return None

    if len(course_code) != 3:  # Legon course codes have 3 characters.
        return None

    cleaned_user_input = course_name + " " + course_code
    logger.info(
        f"User input has been changed from {past_question_name} to {cleaned_user_input}"
    )

    return cleaned_user_input


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    It takes the user's choice and returns a past question assigned to their choice.

    Args:
      update (Update): Update
      context (ContextTypes.DEFAULT_TYPE): ContextTypes.DEFAULT_TYPE

    Returns:
      The past question file.
    """
    choice = update.callback_query
    await choice.answer()
    if choice.data == "-1":
        await context.bot.send_message(
            chat_id=await get_chat_id(update, context),
            text="You selected all.",
        )
    else:
        await context.bot.send_message(
            chat_id=await get_chat_id(update, context),
            text=f"You selected #{choice.data}",
        )

    past_question_links = Scrapper.get_links_of_past_question()
    if len(past_question_links) == 0:
        return await error_handler(
            update, context, False, "Failed to extract past question links."
        )

    await context.bot.send_message(
        chat_id=await get_chat_id(update, context), text="Downloading past question..."
    )

    try:
        gen_file_path = Scrapper.get_past_question(
            past_question_links, choice.data
        )
        if gen_file_path is None:
            return await error_handler(
                update, context, False, "Failed to download file and upload file."
            )

        await context.bot.send_message(
            chat_id=await get_chat_id(update, context),
            text="Uploading past question...",
        )
        for _ in range(len(past_question_links)):
            await context.bot.sendDocument(
                chat_id=await get_chat_id(update, context),
                document=open(next(gen_file_path), "rb"),
            )
    except Exception:
        return await error_handler(
            update, context, False, "Failed to download past question."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    options: List[List] = [[], []]

    await update.message.reply_text(f"You said {update.message.text}.")
    cleaned_user_input = validate_user_input(update.message.text)
    if cleaned_user_input is None:
        return await update.message.reply_text(
            "Please enter a valid past question name (eg. dcit 103, math 122)."
        )
    await update.message.reply_text(
        f"Searching database for {cleaned_user_input} past questions..."
    )

    # Change to saving in s3 bucket
    path = (
        os.getcwd()
        + "\\past_questions\\"
        + update.message.chat.username
        + "_"
        + str(await get_chat_id(update, context))
    )
    scapper = Scrapper(path)
    if scapper.logged_in is False:
        return await error_handler(update, context, False, "Failed to log in.")

    logger.info(
        f"{update.message.from_user.username} is searching for {cleaned_user_input}."
    )

    if scapper.search_for_past_question(cleaned_user_input) == 1:
        return await update.message.reply_text(
            f"Error searching for {cleaned_user_input}. Try again."
        )

    past_question_list = scapper.get_list_of_past_question()
    if (
        len(past_question_list) == 0
    ):
        return await update.message.reply_text(
            f"Unfortunately, there are no {cleaned_user_input} past questions."
        )

    await update.message.reply_text(
        f"We found {len(past_question_list)} {cleaned_user_input} past questions."
    )
    result = scapper.past_question_list_to_string(past_question_list)
    await update.message.reply_text(result)  # display available past questions.

    for past_question_index in range(len(past_question_list)):
        if past_question_index < 5:
            options[0].append(
                InlineKeyboardButton(
                    text=str(past_question_index + 1),
                    callback_data=str(past_question_index + 1),
                )
            )
        else:
            options[1].append(
                InlineKeyboardButton(
                    text=str(past_question_index + 1),
                    callback_data=str(past_question_index + 1),
                ),
            )
    options[1].append(InlineKeyboardButton(text="All", callback_data=str(-1)))

    reply_markup = InlineKeyboardMarkup(options)

    await context.bot.send_message(
        chat_id=await get_chat_id(update, context),
        text="Which one do you want to download?",
        reply_markup=reply_markup,
    )


async def error_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    *args,
    automated_caller: bool = True,
    issue: str = "None",
) -> None:
    """Log the error and send a telegram message to notify the developer."""
    if not automated_caller:
        message = (
            f"An exception was raised while handling an update\n"
            f"User's text: {update.message.text}\n"
            f"User's id: {update.message.from_user.id}\n"
            f"User's first_name: {update.message.from_user.first_name}\n"
            f"User's last_name: {update.message.from_user.last_name}\n"
            f"User's username: {update.message.from_user.username}\n"
            f"What's the issue: {issue}\n"
            f"Automated message?: {automated_caller}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        logger.exception("Exception while handling an update.")
        await context.bot.send_message(
            chat_id=await get_chat_id(update, context),
            text="Unexpected error occurred. Try again. If error persists contact @Daquiver.",
        )
    else:
        message = (
            f"Automated message?: {automated_caller}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        logger.error("A logical error occurred:", issue)
        await context.bot.send_message(
            chat_id=await get_chat_id(update, context),
            text="Unexpected error. Try again. If error persists contact @Daquiver.",
        )

    await context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message)

def start_app(app: ApplicationBuilder) -> None:
    app.add_handler(telegram.ext.CommandHandler("start", start))
    app.add_handler(telegram.ext.CommandHandler("help", help))
    app.add_handler(telegram.ext.CommandHandler("about", about))
    app.add_handler(telegram.ext.CommandHandler("donate", donate))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(telegram.ext.CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    app.add_error_handler(error_handler)



def main():
    logger.info("Starting Application")
    app = ApplicationBuilder().token(TOKEN).build()

    if ENV == "DEV" or ENV == "STG":
        start_app(app)
        app.run_polling()

    else:
        app.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url="https://past-questions-bot.herokuapp.com/" + TOKEN, # change to fly.io public url
    )


if __name__ == "__main__":
    root_logger = logging.getLogger("")
    if not root_logger.handlers:
        root_logger.addHandler(logging.StreamHandler(sys.stdout))

    for name in APPLICATIONS:
        logging.getLogger(name).setLevel(LOG_LEVEL)

    main()