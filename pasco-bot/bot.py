"""Bot File"""
import logging
import os
import sqlite3
from telegram import Update
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext, ApplicationBuilder
from dotenv import load_dotenv


load_dotenv()

# logger for bot
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for conversation
SELECTING_ACTION, SEARCH, SELECT_QUESTION = range(3)

# Create and initialize SQLite database
conn = sqlite3.connect('past_questions.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS past_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_title TEXT NOT NULL,
    question_file BLOB NOT NULL
)
''')
conn.commit()

mock_past_questions = [
    {"title": "DCIT 305 10960584", "file_path": "/home/ephraim/Downloads/Telegram Desktop/DCIT 305 10960584.pdf"},   
    {"title": "Reaction towards AI being controlled", "file_path": "/home/ephraim/Downloads/Telegram Desktop/Reaction+towards+AI+being+controlled.pdf"},
    {"title": "DCIT208 CP-TEAM 35 - SPRINT REPORT 2", "file_path": "/home/ephraim/Downloads/Telegram Desktop/DCIT208 CP-TEAM 35 - SPRINT REPORT 2.pdf"},
    {"title": "Dcit 208 Group 28 Assignment 4.pdf", "file_path": "/home/ephraim/Downloads/Telegram Desktop/Dcit 208 Group 28 Assignment 4.pdf"},
]

# Mock Database with Files
for question in mock_past_questions:
    with open(question["file_path"], "rb") as file:
        cursor.execute("INSERT INTO past_questions (question_title, question_file) VALUES (?, ?)",
                       (question["title"], file.read()))
    conn.commit()

async def start(update: Update, context: CallbackContext):
    """
    Command to start the bot.
    Args:
        update (telegram.Update): The incoming update from the user.
        context (telegram.ext.CallbackContext): The context for this callback function.
    Returns:
        None

    This function is the entry point for the bot and is triggered when the user sends the "/start" command.
    """
    logger.info(f"{update.message.from_user.username} started the bot.")
    await update.message.reply_text(f"""
    Hello {update.message.from_user.username}
Welcome to Past Questions bot"""
)

async def search(update: Update, context: CallbackContext):
    """
    Command to initiate a search for past questions based on a user-provided id.
    Args:
        update (telegram.Update): The incoming update from the user.
        context (telegram.ext.CallbackContext): The context for this callback function.
    Returns:
        int: The next conversation state (in this case, `SEARCH`).
    This function is called when the user sends the "/search" command. It prompts the user to enter a id for searching past questions.
    Upon receiving the id, it initiates the search process and transitions to the `SEARCH` state for further interaction.
    """
    await update.message.reply_text("Please enter a id to search for past questions.")
    return SEARCH

async def search_past_questions(update: Update, context: CallbackContext):
    """
    Perform a search for past questions based on a user-provided id and present the matching past questions.
    Args:
        update (telegram.Update): The incoming update from the user.
        context (telegram.ext.CallbackContext): The context for this callback function.
    Returns:
        int: The next conversation state (either `SELECT_QUESTION` or `ConversationHandler.END`).
    This function is called in response to the user providing a id for searching past questions. It performs a database query to find past questions whose titles match the id.
    If matching questions are found, it presents them to the user and prompts the user to select a past question.
    If no matching questions are found, it informs the user and ends the conversation.
    The function returns the next conversation state, which can be either `SELECT_QUESTION` (if matching questions were found) or `ConversationHandler.END` (if no matching questions were found).
    """
    id = await update.message.text.lower()
    logger.info(f"{update.message.from_user.username} search for past question with id: {id}")

    cursor.execute("SELECT question_title FROM past_questions WHERE question_title LIKE ?", (f'%{id}%',))
    matching_questions = cursor.fetchall()

    if matching_questions:
        await update.message.reply_text("Matching past questions:")
        for i, (question_title,) in enumerate(matching_questions, start=1):
            await update.message.reply_text(f"{i}. {question_title}")

        await update.message.reply_text("Please select a past question by typing its number (e.g., '1' for the first question).")
        context.user_data["matching_questions"] = matching_questions
        return SELECT_QUESTION
    else:
        await update.message.reply_text("No matching past questions found. Please try another id or type /cancel to exit.")
        return ConversationHandler.END

async def list_all_past_questions(update: Update, context: CallbackContext):
    """
    List all available past questions stored in the database.
    Args:
        update (telegram.Update): The incoming update from the user.
        context (telegram.ext.CallbackContext): The context for this callback function.
    Returns:
        None
    This function is triggered when the user sends the "/list" command to list all available past questions.
    It queries the database to retrieve all past questions and their titles. If past questions are found, it sends a list of available past questions to the user.
    If no past questions are found, it informs the user that there are no past questions in the database.
    """
    cursor.execute("SELECT question_title FROM past_questions")
    all_questions = cursor.fetchall()

    if all_questions:
        messages = ["All available past questions:"]
        for i, (question_title,) in enumerate(all_questions, start=1):
            messages.append(f"{i}. {question_title}")
        await update.message.reply_text('\n'.join(messages))
    else:
        await update.message.reply_text("No past questions found in the database.")

async def deliver_past_question(update: Update, context: CallbackContext):
    """
    Deliver the selected past question to the user.
    Args:
        update (telegram.Update): The incoming update from the user.
        context (telegram.ext.CallbackContext): The context for this callback function.
    Returns:
        int: The next conversation state (either `SELECT_QUESTION` or `ConversationHandler.END`).
    This function is called when the user selects a past question by typing a number (e.g., '1' for the first question) in response to the list of matching past questions.
    It attempts to deliver the selected past question to the user as a document.
    If the selection is valid and a matching past question is found, it sends the question as a document.
    If the selection is invalid or an error occurs, it informs the user and provides guidance.
    The function returns the next conversation state, which can be either `SELECT_QUESTION` (if the user continues interacting) or `ConversationHandler.END` (if the conversation ends).
    """
    try:
        selected_id = int(update.message.text)
        cursor.execute("SELECT question_title, question_file FROM past_questions WHERE id = ?", (selected_id,))
        question_data = cursor.fetchone()

        if question_data:
            selected_question_title, question_file = question_data

            # Send the question as a document
            await update.message.reply_document(document=question_file, filename=f"{selected_question_title}")
        else:
            raise ValueError("Invalid selection")

        return ConversationHandler.END
    except (ValueError, IndexError):
        await update.message.reply_text("Invalid selection. Please select a valid ID from the list or type /start to restart.")
        return SELECT_QUESTION

async def help(update: Update, context: CallbackContext):
    """
    Command to display the list of available commands.
    Args:
        update (telegram.Update): The incoming update from the user.
        context (telegram.ext.CallbackContext): The context for this callback function.
    Returns:
        None

    This function is triggered when the user sends the "/help" command. It provides the user with a list of available commands.
    """
    help_text = "Available commands:\n" \
                "/start - Start the bot and get a welcome message\n" \
                "/search - Search for past questions based ID\n" \
                "/list - List all available past questions\n" \
                "/help - Display this help menu"

    await update.message.reply_text(help_text)

async def error(update: Update, context: CallbackContext):
    """Error Handling"""
    logger.error(f"An error occurred: {context.error}")
    await update.message.reply_text("An error occurred. Please type /start to restart the conversation.")
    return ConversationHandler.END

def main():
    """Starts The Bot"""
    app = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start), CommandHandler('list', list_all_past_questions)],
    states={
        SELECTING_ACTION: [CommandHandler('search', search)],
        SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_past_questions)],
        SELECT_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, deliver_past_question)],
    },
    fallbacks=[],
    allow_reentry=True)

    app.add_handler(conv_handler)
    app.add_handler(telegram.ext.CommandHandler("start", start))
    app.add_handler(telegram.ext.CommandHandler("search", search))
    app.add_handler(telegram.ext.CommandHandler("list", list_all_past_questions))
    app.add_handler(telegram.ext.CommandHandler("help", help))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), deliver_past_question))
    app.add_error_handler(error)

    app.run_polling()

if __name__ == '__main__':
    main()