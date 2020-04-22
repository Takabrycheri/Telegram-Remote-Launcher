import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os
import threading

TOKEN = ''

path_notepad = "C:\\Windows\\System32\\notepad.exe"

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there :D")

def shutdown():
    updater.stop()
    updater.is_idle = False
    quit()

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot turned off!")
    threading.Thread(target=shutdown).start()

def notepad(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Launching Notepad on PC...")
    try:
        os.startfile(path_notepad)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Notepad launched :)")
    except Exception:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Notepad failed to launch :(")

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unkown command :(")

start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
notepad_handler = CommandHandler('notepad', notepad)
unknown_handler = MessageHandler(Filters.text | Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(notepad_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()