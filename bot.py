import telegram.ext
from test import search_for_pasco

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

def contact(update, context):
	update.message.reply_text(f"""
		You can contact me through the following
		Gmail: Cabrokwa11@gmail.com
		Telegram: @Daquiver
		Github: https://github.com/Daquiver1
		""")

def handle_message(update, context):
	update.message.reply_text(f"You said {update.message.text}")
	search_for_pasco(update.message.text)
	return type(update.message.text)

updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.CommandHandler("contact", contact))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()
