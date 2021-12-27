import telegram.ext
from telegram.ext import CallbackQueryHandler
from test import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
PATH = "C:\\Users\\Anita Agyepong\\Documents\\Daquiver's Quivers\\Python\\past_questions_bot\\past_questions"


with open("token.txt", "r") as token:
	TOKEN = token.read()

def start(update, context):
	update.message.reply_text(f"""
		Hello (insert user's name) Welcome to Daquiver's Past Question bot
		This bot is simple. 
		Type the name of the past question you want.
		""")

def help(update, context):
	update.message.reply_text("""
	The following commands are available:

	/start -> Welcome Message
	/help -> This Message
	/contact -> Contact Owner
	""")
def get_chat_id(update, context):
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

def contact(update, context):
	update.message.reply_text(f"""
		You can contact me through the following
		Gmail: Cabrokwa11@gmail.com
		Telegram: @Daquiver
		Github: https://github.com/Daquiver1
		""")

def button(update, context):
	choice = update.callback_query
	choice.answer()
	choice.edit_message_text(text=f"Selected option: {choice.data}")
	site = link_of_pasco()
	download_pasco(site, choice.data)
	#file = PATH + "\\" + 
	file = "C:\\Users\\Anita Agyepong\\Documents\\Daquiver's Quivers\\Python\\past_questions_bot\\past_questions\\law.pdf"
	context.bot.sendDocument(chat_id=get_chat_id(update, context), document=open(file, 'rb'))


def handle_message(update, context):
	update.message.reply_text(f"You said {update.message.text}")
	search_for_pasco(update.message.text)
	lists = display_pascos()
	options = []
	for i in range(len(lists) - 1):
		update.message.reply_text(str(i+1) + " " + lists[i])
		options.append(InlineKeyboardButton(text=str(i+1), callback_data=str(i+1)))

	reply_markup = InlineKeyboardMarkup([options])
	context.bot.send_message(chat_id=get_chat_id(update, context), text='What would you like to download?', reply_markup=reply_markup)


updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(CallbackQueryHandler(button))
disp.add_handler(telegram.ext.CommandHandler("contact", contact))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()
