# import everything
from flask import Flask, request
import telegram
from thebot.bot import get_response
from thebot.credentials import bot_token, URL

global TOKEN
global bot 
TOKEN = bot_token
bot = telegram.Bot(token = TOKEN)

# Start the flask app
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
	# retrieve the message in JSON and then transform it to Telegram object
	update = telegram.Update.de_json(request.get_json(force=True), bot)

	# get the chat_id to be able to respond to the same user
	chat_id = update.message.chat.id

	# get the message id to be able to reply to this specific message
	msg_id = update.message.message_id

	# Telegram understands UTF-8, so encode text for unicode compatibility
	text = update.message.text.encode('utf-8').decode()
	print("got text message :", text)

	# here we call our super AI
	response = get_response(text)
	#response = handle_message(text)
	# now just send the message back
	# notice how we specify the chat and the msg we reply to
	bot.sendMessage(chat_id=chat_id, text=response, reply_to_message_id=msg_id)

	return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return "This is the home page. Testing 12"

if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)