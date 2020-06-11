import logging
from flask import Flask, request
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update
from utils import get_reply, fetch_news
#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

Token = "Token Goes Here"

app  = Flask(__name__)
@app.route('/')
def index():
    return "Hello"

@app.route(f'/{Token}', methods = ['GET', 'POST'])
def webhook():
    """webhook view which recieves updates from telegram"""
    update = Update.de_json(request.get_json(),bot)
    dp.process_update(update)
    return "ok"

def start(bot,update):
    print(update)
    author = update.message.from_user.first_name
    #msg = update.message.text
    reply = "Hi! {}".format(author)
    bot.send_message(chat_id = update.message.chat_id, text = reply)

def help(bot,update):
    help_text = "Hey How can I help?"
    bot.send_message(chat_id = update.message.chat_id, text = help_text)

def reply_text(bot,update):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    if(intent=='get_news'):
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id = update.message.chat_id, text = article['link'])
    else:
        bot.send_message(chat_id = update.message.chat_id, text = reply)

def echo_sticker(bot,update):
    bot.send_sticker(chat_id = update.message.chat_id, sticker=update.message.sticker.file_id)

def error(bot,update):
    logger.error("Update '%s' caused error '%s'", update, update.error)


if __name__ == "__main__":
    bot = Bot(Token)
    bot.set_webhook("https://48d6ca427675.ngrok.io/" + Token)

    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)
    app.run(port=8443)
