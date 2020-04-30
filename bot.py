import threading
import logging
import os
import settings

try:
    import telegram
    from telegram.ext import Updater
    from telegram.ext import CommandHandler
    from telegram.ext import MessageHandler, Filters
except ImportError:
    print("Dependencies have not been installed...")
    print("Restart me when the other cmd disappears")
    os.startfile("requirements.bat")
    quit()

current_version = 2
try:
    settings_version = settings.settings_version
except AttributeError:
    print("--------------------------------------")
    print("The settings.py file is the first version, you have to update it!")
    print("Current version: " + str(current_version))
    print("--------------------------------------")
    quit()

if current_version != settings_version:
    print("--------------------------------------")
    print("You need to update the settings.py file!")
    print("Settings version: " + str(settings_version))
    print("New version: " + str(current_version))
    print("--------------------------------------")
    quit()

if settings.token == '':
    print("--------------------------------------")
    print("Insert your BotFather token in settings.py!")
    print("--------------------------------------")
    quit()

if settings.user_id == '':
    print("--------------------------------------")
    print("Insert your user id in settings.py")
    print("If you don't know it send a message to bot, it will reply with your user id")
    print("--------------------------------------")

updater = Updater(token=settings.token, use_context=True)
dispatcher = updater.dispatcher

print("Bot online!")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def checkUser(update, context):
    user = update.message.from_user
    if settings.user_id == '':
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<i>Hi %s, before you can do any command you must enter your user id in the settings.py file to prevent strangers from sending commands to your PC!</i>\n\n<b>Here is your user ID:</b> <code>%s</code>\n<i>(click it to copy)</i>" % (user['first_name'], user['id']))
        reason = "auto_shutdown"
        threading.Thread(target=shutdown, args=(context, update, reason)).start()
        return False
    elif str(user['id']) != settings.user_id:
        return False
    else:
        return True

def start(update, context):
    if checkUser(update, context) is True:
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Hello there :D")

def shutdown(context, update, reason):
    if reason == "cmd_stop":
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Bot turned off!")
    if reason == "auto_shutdown":
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="I am automatically turning off to allow you to make the change :)")

    updater.stop()
    updater.is_idle = False
    print("The bot has been shut down!")
    quit()

def stop(update, context):
    if checkUser(update, context) is True:
        reason = "cmd_stop"
        threading.Thread(target=shutdown, args=(context, update, reason)).start()

def open(update, context):
    if checkUser(update, context) is True:
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
    if checkUser(update, context) is True:
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
    if checkUser(update, context) is True:
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