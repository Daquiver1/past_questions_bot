import telegram.ext
from telegram.ext import CallbackQueryHandler
#from test import *
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "5092060662:AAGbACVVEUlo67Up4Xyh7v3dMjf61MOMisI"

def start(update, context):
	update.message.reply_text(f"""
		Hello {update.message.from_user.username}
		Welcome to Daquiver's Past Question bot
		This bot is simple. 
		Type the name of the past question you want and you are good to go. 
		Use this format (eg. ugbs 104, dcit 103)
		""")

def help(update, context):
	update.message.reply_text("""
	The following commands are available:

	/start -> Welcome Message
	/help -> This Message
	/contact -> Contact Owner
	/donate -> Buy me a drink.
	""")

def donate(update, context):
	update.message.reply_text(f"""
		Telegram api has no support for mobile money or other popular payments, so you'll have to do it the old way. 
		The number is 0547642843
		""")

# def get_chat_id(update, context):
#     chat_id = -1

#     if update.message is not None:
#         # text message
#         chat_id = update.message.chat.id
#     elif update.callback_query is not None:
#         # callback message
#         chat_id = update.callback_query.message.chat.id
#     elif update.poll is not None:
#         # answer in Poll
#         chat_id = context.bot_data[update.poll.id]

#     return chat_id

# def clean_name(pasco_name):
# 	"""
# 	A function to ask user for name of past_question.
# 	It takes in the course name and course code.
# 	It returns the the course name and course code concatenated.

# 	Output: String type.
# 	"""
# 	if len(pasco_name.split()) == 1:		# numbers and text combined(no space)
# 		temp = re.compile("([a-zA-Z]+)([0-9]+)")
# 		res = temp.match(pasco_name)
# 		if res == None:
# 			return res
# 		res = res.groups()
# 	else:
# 		res = pasco_name.split()

# 	pasco_name = res[0]
# 	pasco_code = res[-1]

# 	if pasco_name.isalpha() == False:
# 		res = None
# 		return res

# 	if len(pasco_name) != 4:	# Legon course names have 4 characters.
# 		res = None
# 		return res 

# 	if pasco_code.isnumeric() == False:
# 		res = None
# 		return res

# 	if len(pasco_code) != 3:	# Legon course codes have 3 characters.
# 		res = None
# 		return res			

# 	pasco = pasco_name + " " + pasco_code 	# The site's search won't work if it isn't spaced.
# 	return pasco


def contact(update, context):
	update.message.reply_text(f"""
		You can contact me through the following
		Gmail: Cabrokwa11@gmail.com
		Telegram: @Daquiver
		Github: https://github.com/Daquiver1
		""")

# def button(update, context):
# 	choice = update.callback_query
# 	choice.answer()
# 	site = link_of_pasco()
# 	choice.edit_message_text(text=f"Selected option: {choice.data}")
# 	choice.edit_message_text("Downloading past question, gimme a sec")
# 	try:
# 		file = download_pasco(site, choice.data)
# 		choice.edit_message_text("Uploading past question, gimme a sec")
# 		context.bot.sendDocument(chat_id=get_chat_id(update, context), document=open(file, 'rb'))
# 	except OSError:
# 		choice.edit_message_text("Yikes, we encountered an error. Try again. If it persists view the help command and contact me.")


# def handle_message(update, context):
# 	options = []
# 	update.message.reply_text(f"You said {update.message.text}")
# 	name12 = clean_name(update.message.text)
# 	if name12 == None:
# 		update.message.reply_text("Please enter a valid past question name (eg. ugbs 104, dict 202)")
# 		return None

# 	update.message.reply_text(f"Checking for {name12} past questions")
# 	time.sleep(1)
# 	search_for_pasco(name12)
# 	lists = display_pascos()
# 	if len(lists) == 0:
# 		update.message.reply_text(f"Unfortunately, there are no past questions available for {name12}")
# 		return None

# 	update.message.reply_text("Yaay!!, we got some.")
# 	for i in range(len(lists) - 1):
# 		update.message.reply_text(str(i+1) + " " + lists[i])
# 		options.append(InlineKeyboardButton(text=str(i+1), callback_data=str(i+1)))

# 	reply_markup = InlineKeyboardMarkup([options])
# 	context.bot.send_message(chat_id=get_chat_id(update, context), text='What would you like to download?', reply_markup=reply_markup)


updater = telegram.ext.Updater(TOKEN, use_context=True)
disp = updater.dispatcher
disp.add_handler(telegram.ext.CommandHandler("start", start))
disp.add_handler(telegram.ext.CommandHandler("help", help))
disp.add_handler(telegram.ext.CommandHandler("donate", donate))
#disp.add_handler(CallbackQueryHandler(button))
disp.add_handler(telegram.ext.CommandHandler("contact", contact)) 
#disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))

# updater.start_polling()
# updater.idle()

def get_response(msg):
    """
    you can place your mastermind AI here
    could be a very basic simple response like "معلش"
    or a complex LSTM network that generate appropriate answer
    """
    return contact(update, context)