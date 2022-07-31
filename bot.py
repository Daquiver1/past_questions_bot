import telegram.ext, os
from telegram.ext import CallbackQueryHandler
from test import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
PORT = int(os.environ.get("PORT", "8443"))


TOKEN = os.environ.get("TOKEN")

def start(update, context):
	"""
	Start command
	"""

	update.message.reply_text(f"""
		Hello {update.message.from_user.username}
		Welcome to Daquiver's Past Question bot
		Please check out the /about section before you begin.
		This bot is simple. 
		Type the name of the past question you want and you are good to go. 
		Use this format (eg. ugbs 104, dcit 103)
		""")

def help(update, context):
	"""
	Help command
	"""

	update.message.reply_text("""
	The following commands are available:

	/start -> Welcome Message
	/help -> This Message
	/contact -> Contact Owner
	/donate -> Buy me a drink.
	/about -> Why was this bot built?
	""")

def donate(update, context):
	"""
	Donate command
	"""

	update.message.reply_text(f"""
		Number: 0547642843
		""")

def contact(update, context):
	"""
	Contact command
	"""

	update.message.reply_text(f"""
		You can contact me through the following
		Gmail: Cabrokwa11@gmail.com
		Telegram: @Daquiver
		Github: https://github.com/Daquiver1
		""")

def about(update,context):
	"""
	About command
	"""

	update.message.reply_text(f"""
		Okay so this is a simple bot nothing fancy or anything, it basically scrapes the ug past questions site(https://balme.ug.edu.gh/past.exampapers/index.php)
		and returns the past question.
		It can only download past questions on the ug site. If the past question isn't available then legon haven't uploaded it to their site.
		I built it because students find it difficult to access the site(you need to register) and also most don't know about the site(weird, I know), 
		so this is a simplified version. Also I knew building this will challenge me and make me a better developer(it did.) So yeah. 
		""")


def get_chat_id(update, context):
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

def clean_name(pasco_name):
	"""
	A function that returns the cleaned name of user's text.
	Returns None if user doesn't satisfy a criteria.

	Output: String type.
	"""

	if len(pasco_name.split()) == 1:		# if it's numbers and text combined(no space)
		temp = re.compile("([a-zA-Z]+)([0-9]+)")
		res = temp.match(pasco_name)
		if res == None:
			return res
		res = res.groups()
	else:
		res = pasco_name.split()

	pasco_name = res[0]			# Course name
	pasco_code = res[-1]		# Course code

	if pasco_name.isalpha() == False:
		res = None
		return res

	if len(pasco_name) != 4:	# Legon course names have 4 characters.
		res = None
		return res 

	if pasco_code.isnumeric() == False:
		res = None
		return res

	if len(pasco_code) != 3:	# Legon course codes have 3 characters.
		res = None
		return res			

	pasco = pasco_name + " " + pasco_code 	# The site's search won't work if it isn't spaced.
	return pasco


def button(update, context):
	"""
	Callback function, takes the user's choice and returns a past question assigned to their choice.
	"""
	choice = update.callback_query
	choice.answer()			# callback queries have to be answered. (don't fully understand why)
	site = link_of_pasco()
	choice.edit_message_text(text=f"Selected option: {choice.data}")
	choice.edit_message_text("Downloading past question, gimme a sec")
	try:
		file = download_pasco(site, choice.data)
		choice.edit_message_text("Uploading past question, gimme a sec")
		context.bot.sendDocument(chat_id=get_chat_id(update, context), document=open(file, 'rb'))
	except:
		choice.edit_message_text("Yikes, we encountered an error. Try again.\n If error persists contact @Daquiver")


def handle_message(update, context):
	"""
	A function to handle user messages. 
	Takes the text and returns options of the avaliable of the text. 
	Assuming it matched the criteria specified in clean_name()
	"""

	options = []
	update.message.reply_text(f"You said {update.message.text}")
	update.message.reply_text("Sorry for any inconvenience caused. We are currently under maintenance. Contact @Daquiver for more information.")
	# new_text = clean_name(update.message.text)
	# if new_text == None:
	# 	update.message.reply_text("Please enter a valid past question name (eg. ugbs 104, dict 202)")
	# 	return None

	# update.message.reply_text(f"Checking for {new_text} past questions")
	# time.sleep(1)
	# search_for_pasco(new_text)
	# lists = display_pascos()
	# if len(lists) == 0:				# Check if there are past questions available for users text.
	# 	update.message.reply_text(f"Unfortunately, there are no past questions available for {new_text}")
	# 	return None

	# update.message.reply_text("Yaay! we got some.")

	# for i in range(len(lists)):
	# 	update.message.reply_text(str(i+1) + " " + lists[i])	# display available past questions.
	# 	options.append(InlineKeyboardButton(text=str(i+1), callback_data=str(i+1)))

	# reply_markup = InlineKeyboardMarkup([options])
	# context.bot.send_message(chat_id=get_chat_id(update, context), text='Which one do you want to download?', reply_markup=reply_markup)

def main(): 
	updater = telegram.ext.Updater(TOKEN, use_context=True)
	disp = updater.dispatcher
	disp.add_handler(telegram.ext.CommandHandler("start", start))
	# disp.add_handler(telegram.ext.CommandHandler("help", help))
	# disp.add_handler(telegram.ext.CommandHandler("about", about))
	# disp.add_handler(telegram.ext.CommandHandler("donate", donate))
	# disp.add_handler(CallbackQueryHandler(button))
	# disp.add_handler(telegram.ext.CommandHandler("contact", contact)) 
	disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

	# for polling
	#updater.start_polling()
	#"""
	updater.start_webhook(listen="0.0.0.0",
							port = PORT,
							url_path=TOKEN,
							webhook_url= "https://past-questions-bot.herokuapp.com/" + TOKEN)
	#"""
	updater.idle()

if __name__ == '__main__':
	main()
