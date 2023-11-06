from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

default_context_type = ContextTypes.DEFAULT_TYPE
from .responses import start_message

async def start(update: Update, context: CallbackContext):
    """Start command"""
    user = update.effective_user
    user_id = user.id
    user_name = user.name
    if user_name:
        await update.message.reply_text(f'Hi {user_name}')
    await context.bot.send_message(user_id, start_message)


async def handle_message(update: Update, context: default_context_type):
    pass

async def help(update: Update, context: default_context_type):
    pass

async def about(update: Update, context: default_context_type):
    pass

async def search():
    pass

async def year():
    pass


async def error_handler(update: Update, context: default_context_type, *args, issue: str = 'None') -> None:
    pass