"""Main bot file."""
import logging
import os
import re
from typing import Any, List, Match, Union

import telegram.ext
from functions import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")
PORT = int(os.environ.get("PORT", "8443"))
TOKEN = os.environ.get("TOKEN")


def start(update: Update, context: Any) -> None:
    """
    Start command
    """

    update.message.reply_text(
        f"""
	Hello {update.message.from_user.username}
	Welcome to Daquiver's Past Questions bot

	This bot is simple.
	Type the name of the past question, select the one you want and it'll be sent to you.
	Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 )
	Check out the /about section for more info.

		"""
    )


def help(update: Update, context: Any) -> None:
    """
    Help command
    """

    update.message.reply_text(
        """
	The following commands are available:

	/donate -> Buy me a drink.
	/start -> Welcome Message.
	/help -> This Message.
	/contact -> My contact details.
	/about -> Why did I build this?
	"""
    )


def donate(update: Update, context: Any) -> None:
    """
    Donate command
    """

    update.message.reply_text(
        "Thanks for donating. Details below.\nName: Christian Abrokwa\nNumber: 0547642843"
    )


def contact(update: Update, context: Any) -> None:
    """
    Contact command
    """

    update.message.reply_text(
        f"""
		You can contact me vai the following
		Gmail: Cabrokwa11@gmail.com

		Telegram: @Daquiver

		Github: https://github.com/Daquiver1

		Twitter: https://www.twitter.com/daquiver1

		LinkedIn: https://www.linkedin.com/in/daquiver
		"""
    )


def about(update: Update, context: Any) -> None:
    """
    About command
    """

    update.message.reply_text(
        f"""
		Hey I'm Christian, Christian Abrokwa. A student of the University of Ghana. During the day I'm a software engineer and in the nights I'm a superhero. Somewhere in between, I'm a student.\nSo why did I build this?

		I noticed there was a bottleneck with the current system of getting a past question. It took a student about a week to get access to a past question.
		So, I built and developed this system which allows University of Ghana students to download past questions under 30 seconds.

    It works by scraping the ug past questions site(https://balme.ug.edu.gh/past.exampapers/index.php) and returning files matching the users criteria.

    It can only download past questions on the ug site. So if a past question isn't found, it means the University haven't uploaded the past question.

    * This bot was built on Janurary 4th, 2022.
		"""
    )


def get_chat_id(update: Update, context: Any) -> int:
    """
    A function that returns the chat id of the user
    """

    chat_id = -1

    if update.message is not None:
        # text message
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        # callback message
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        # answer in Poll
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def validate_user_input(past_question_name: str) -> Union[Match[str], Any]:
    """
    A function that returns the cleaned name of user's text.
    Returns None if user input doesn't satisfy a criteria.

    Output: String type.
    """

    if (
        len(past_question_name.split()) == 1
    ):  # if it's numbers and text combined(no space)
        temp = re.compile("([a-zA-Z]+)([0-9]+)")
        result = temp.match(past_question_name)
        if result:
            result = result.groups()
        else:
            return result
    else:
        result = past_question_name.split()

    course_name = result[0]  # Course name
    course_code = result[-1]  # Course code

    if course_name.isalpha() == False:
        return None

    if len(course_name) != 4:  # Legon course names have 4 characters.
        return None

    if course_code.isnumeric() == False:
        return None

    if len(course_code) != 3:  # Legon course codes have 3 characters.
        return None

    cleaned_user_input = course_name + " " + course_code
    logging.info(
        f"User input has been changed from {past_question_name} to {cleaned_user_input}"
    )
    # The site's search won't work if it isn't spaced.
    return cleaned_user_input


def button(update: Update, context: Any) -> None:
    """
    Callback function, takes the user's choice and returns a past question assigned to their choice.
    """
    choice = update.callback_query
    choice.answer()  # callback queries have to be answered. (don't fully understand why)
    past_question_links = get_links_of_past_question()
    if len(past_question_links) == 0:
        update.message.reply_text(
            "Unexpected error. Please try again. If error persists contact @Daquiver."
        )
        return None

    update.send_message_text(f"You selected {choice.data}_update")
    update.send_message_text(f"Downloading past question(s)_update")
    choice.edit_message_text(text=f"You selected {choice.data}")
    choice.edit_message_text("Downloading past question...")
    try:
        file = get_past_question(past_question_links, choice.data)
        choice.edit_message_text("Uploading past question...")
        update.send_message_text(f"Uploading past question(s)_update")

        for i in file:
            context.bot.sendDocument(
                chat_id=get_chat_id(update, context), document=open(i, "rb")
            )
    except:
        logging.error("Failed to download past question", exc_info=True)
        choice.edit_message_text(
            "Unexpected error. Try again.\n If error persists contact @Daquiver."
        )
        update.send_message_text(
            f"Unexpected error. Try again.\n If error persists contact @Daquiver."
        )


def handle_message(update: Update, context: Any) -> None:
    """
    A function to handle user messages.
    Takes the text and returns options of the avaliable of the text.
    Assuming it matched the criteria specified in clean_name()
    """
    global chat_id
    chat_id = get_chat_id(update, context)
    options = []
    update.message.reply_text(f"You said {update.message.text}.")
    cleaned_user_input = validate_user_input(update.message.text)
    if cleaned_user_input == None:
        update.message.reply_text(
            "Please enter a valid past question name (eg. dcit 103, math 122, ugrc 110)."
        )
        return None

    logging.info(
        f"{update.message.from_user.username} is searching for {cleaned_user_input}."
    )
    update.message.reply_text(
        f"Searching database for {cleaned_user_input} past questions."
    )

    if search_for_past_question(cleaned_user_input) == 1:
        update.message.reply_text(
            f"Error searching for {cleaned_user_input}. Try again."
        )
        return None

    past_question_list = get_list_of_past_question()
    if (
        len(past_question_list) == 0
    ):  # Check if there are past questions available for users text.
        update.message.reply_text(
            f"Unfortunately, there are no {cleaned_user_input} past questions."
        )
        return None

    update.message.reply_text(
        f"We found {len(past_question_list)} {cleaned_user_input} past questions."
    )

    for past_question_index in range(len(past_question_list)):
        update.message.reply_text(
            str(past_question_index + 1)
            + ") "
            + past_question_list[past_question_index]
        )  # display available past questions.
        options.append(
            InlineKeyboardButton(
                text=str(past_question_index + 1),
                callback_data=str(past_question_index + 1),
            )
        )
    options.append(InlineKeyboardButton(text="All", callback_data=str(-1)))

    reply_markup = InlineKeyboardMarkup([options])
    context.bot.send_message(
        chat_id=get_chat_id(update, context),
        text="Which one do you want to download?",
        reply_markup=reply_markup,
    )


def main() -> None:
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    disp = updater.dispatcher
    disp.add_handler(telegram.ext.CommandHandler("start", start))
    disp.add_handler(telegram.ext.CommandHandler("help", help))
    disp.add_handler(telegram.ext.CommandHandler("about", about))
    disp.add_handler(telegram.ext.CommandHandler("donate", donate))
    disp.add_handler(CallbackQueryHandler(button))
    disp.add_handler(telegram.ext.CommandHandler("contact", contact))
    disp.add_handler(
        telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message)
    )

    # for polling
    # updater.start_polling()

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url="https://past-questions-bot.herokuapp.com/" + TOKEN,
    )
    updater.idle()


if __name__ == "__main__":
    main()
