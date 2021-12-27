import telegram.ext

with open("token.txt", "r") as token:
	TOKEN = token.read()

def start(update, context):
	update.message.reply_text("Hello! YallWelcome to Daquiver's Past Question bot")

def help(update, context):
	update.message.reply_text("""
	The following commands are available:

	/start -> Welcome Message
	/help -> This Message
	/content -> Information About Daquiver's Bot
	/contact -> Contact Owner
 
	""")

def content(update, context):
	update.message.reply_text("We have books and videos for you to watch.")

def contact(update, context):
	update.message.reply_text("You can contact @Daquiver on my telegram")

def handle_message(update, context):
	update.message.reply_text(f"You said {update.message.text}")

updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.CommandHandler("content", content))
disp.add_handler(telegram.ext.CommandHandler("contact", contact))
disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

updater.start_polling()
updater.idle()
