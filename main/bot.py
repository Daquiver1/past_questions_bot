"""Main bot file."""
import logging
import os
import re
from typing import Any, Awaitable, List, Match, Union

import dotenv
import functions
import telegram.ext
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")
# PORT = int(os.environ.get("PORT", "8443"))
TOKEN = os.getenv("TOKEN")
function_class = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command."""
    await update.message.reply_text(
        f"""
    Hello {update.message.from_user.username}
    Welcome to Daquiver's Past Questions bot

    This bot is simple.
    Type the name of the past question, select the one you want and it'll be sent to you.
    Use this format ( ugbs 104, dcit 103, math 122, ugrc 110 )
    Check out the /about section for more info.

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
        "Thanks for donating. Details below.\nName: Christian Abrokwa\nNumber: 0547642843"
    )


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contact command."""
    await update.message.reply_text(
        """
        You can contact me via the following
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
    Hey I'm Christian, Christian Abrokwa. A student of the University of Ghana. During the day I'm a software engineer and in the nights I'm a superhero. Somewhere in between, I'm a student.\nSo why did I build this?

    I noticed there was a bottleneck with the current system of getting a past question. It took a student about a week to get access to a past question.
    So, I built and developed this system which allows University of Ghana students to download past questions under 30 seconds.

    It works by scraping the ug past questions site(https://balme.ug.edu.gh/past.exampapers/index.php) and returning files matching the users criteria.

    It can only download past questions on the ug site. So if a past question isn't found, it means the University haven't uploaded the past question.

    * This bot was built on January 4th, 2022.
        """
    )


async def get_chat_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[int, str]:
    """A function that returns the chat id of the user."""
    if update.message is not None:
        # text message
        return update.message.chat.id
    elif update.callback_query is not None:
        # callback message
        return update.callback_query.message.chat.id
    elif update.poll is not None:
        # answer in Poll
        return context.bot_data[update.poll.id]

    return -1


def validate_user_input(past_question_name: str) -> Union[str, None]:
    """
    A function that returns the cleaned name of user's text.

    Args:
      past_question_name (str): str
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
    logging.info(
        f"User input has been changed from {past_question_name} to {cleaned_user_input}"
    )
    # The site's search won't work if it isn't spaced.
    return cleaned_user_input


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback function, takes the user's choice and returns a past question assigned to their choice."""
    choice = update.callback_query
    await choice.answer()
    past_question_links = function_class.get_links_of_past_question()
    if len(past_question_links) == 0:
        await update.message.reply_text(
            "Unexpected error. Please try again. If error persists contact @Daquiver."
        )
        return None

    await context.bot.send_message(
        chat_id=await get_chat_id(update, context),
        text=f"You selected #{choice.data}",
    )

    await context.bot.send_message(
        chat_id=await get_chat_id(update, context), text="Downloading past question..."
    )

    try:
        file = function_class.get_past_question(past_question_links, choice.data)
        await context.bot.send_message(
            chat_id=await get_chat_id(update, context),
            text="Uploading past question...",
        )

        await context.bot.sendDocument(
            chat_id=await get_chat_id(update, context), document=open(file, "rb")
        )
    except:
        logging.error("Failed to download past question", exc_info=True)
        await context.bot.send_message(
            chat_id=await get_chat_id(update, context),
            text="Unexpected error. Try again.\n If error persists contact @Daquiver.",
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    A function to handle user messages.
    Takes the text and returns options of the available of the text.
    Assuming it matched the criteria specified in clean_name()
    """
    options = [[], []]
    await update.message.reply_text(f"You said {update.message.text}.")
    cleaned_user_input = validate_user_input(update.message.text)
    if cleaned_user_input == None:
        await update.message.reply_text(
            "Please enter a valid past question name (eg. dcit 103, math 122, ugrc 110)."
        )
        return None
    await update.message.reply_text(
        f"Searching database for {cleaned_user_input} past questions..."
    )
    # Start selenium.
    global function_class
    path = (
        os.getcwd()
        + "\\"
        + update.message.chat.username
        + "_"
        + str(await get_chat_id(update, context))
    )
    function_class = functions.Functions(path)
    logging.info(
        f"{update.message.from_user.username} is searching for {cleaned_user_input}."
    )

    if function_class.search_for_past_question(cleaned_user_input) == 1:
        await update.message.reply_text(
            f"Error searching for {cleaned_user_input}. Try again."
        )
        return None

    past_question_list = function_class.get_list_of_past_question()
    if (
        len(past_question_list) == 0
    ):  # Check if there are past questions available for users text.
        await update.message.reply_text(
            f"Unfortunately, there are no {cleaned_user_input} past questions."
        )
        return None

    await update.message.reply_text(
        f"We found {len(past_question_list)} {cleaned_user_input} past questions."
    )
    text = function_class.clean_past_question_list(past_question_list)
    await update.message.reply_text(text)  # display available past questions.
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
                )
            )

    reply_mar = InlineKeyboardMarkup(options)

    await context.bot.send_message(
        chat_id=await get_chat_id(update, context),
        text="Which one do you want to download?",
        reply_markup=reply_mar,
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(telegram.ext.CommandHandler("start", start))
    app.add_handler(telegram.ext.CommandHandler("help", help))
    app.add_handler(telegram.ext.CommandHandler("about", about))
    app.add_handler(telegram.ext.CommandHandler("donate", donate))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(telegram.ext.CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # for polling
    app.run_polling()

    # updater.start_webhook(
    #     listen="0.0.0.0",
    #     port=PORT,
    #     url_path=TOKEN,
    #     webhook_url="https://past-questions-bot.herokuapp.com/" + TOKEN,
    # )


if __name__ == "__main__":
    main()
