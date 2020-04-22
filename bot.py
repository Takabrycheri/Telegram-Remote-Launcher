try:
    import telegram
    from telegram.ext import Updater
    from telegram.ext import CommandHandler
    from telegram.ext import MessageHandler, Filters
    import threading
    import logging
    import os
    import settings
except ImportError:
    print("The Telegram bot module is not installed, give me a few seconds...")
    print("--------------------------------------")
    
    import pip
    
    pip.main(["install", "python-telegram-bot"])
    
    print("--------------------------------------")
    print("Module installed, bot started!")

    import telegram
    from telegram.ext import Updater
    from telegram.ext import CommandHandler
    from telegram.ext import MessageHandler, Filters
    import threading
    import logging
    import os
    import settings

if settings.token == '':
    print("Insert your BotFather token in settings.py!")
    quit()

updater = Updater(token=settings.token, use_context=True)
dispatcher = updater.dispatcher

print("Bot online!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Hello there :D")

def shutdown():
    updater.stop()
    updater.is_idle = False
    print("The bot has been shut down!")
    quit()

def stop(update, context):
    context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Bot turned off!")
    threading.Thread(target=shutdown).start()

def open(update, context):
    file_name = ' '.join(context.args)
    file_name_c = file_name.capitalize()
    if file_name in settings.files:
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Opening <b>%s</b>" % file_name_c)
        try:
            exec("os.startfile(settings.path_%s)" % file_name)
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> opened" % file_name_c)
            print("Opened %s" % file_name_c)
        except Exception:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> has failed to open :(" % file_name_c)
            print("Failed to open %s" % file_name_c)
    else:
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> is not defined in settings.py" % file_name_c)
        print("Tried to open %s, but is not defined in settings.py" % file_name_c)

def launch(update, context):
    software_name = ' '.join(context.args)
    software_name_c = software_name.capitalize()
    if software_name in settings.softwares:
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Launching <b>%s</b>" % software_name_c)
        try:
            exec("os.startfile(settings.path_%s)" % software_name)
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> launched :)" % software_name_c)
            print("Launched %s" % software_name_c)
        except Exception:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> has failed to launch :(" % software_name_c)
            print("Failed to launch %s" % software_name_c)
    else:
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> is not defined in settings.py" % software_name_c)
        print("Tried to launch %s, but is not defined in settings.py" % software_name_c)

def unknown(update, context):
    context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Unkown command :(")

start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
open_handler = CommandHandler('open', open)
launch_handler = CommandHandler('launch', launch)
unknown_handler = MessageHandler(Filters.text | Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(open_handler)
dispatcher.add_handler(launch_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()