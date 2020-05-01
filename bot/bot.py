import threading
import logging
import os
import json

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

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

cfg_version = 3

if cfg_version != config['config_version']:
    print("--------------------------------------")
    print("You need to update the settings file!")
    print("Settings version: " + str(config['config_version']))
    print("New version: " + str(cfg_version))
    print("--------------------------------------")
    quit()

if config['bot_settings']['token'] == '':
    print("--------------------------------------")
    print("Insert your BotFather token in settings.py!")
    print("--------------------------------------")
    quit()

if config['bot_settings']['user_id'] == '':
    print("--------------------------------------")
    print("Insert your user id in settings.py")
    print("If you don't know it send a message to bot, it will reply with your user id")
    print("--------------------------------------")

# FUNCTIONS #

def checkUser(update, context):
    user = update.message.from_user
    if config['bot_settings']['user_id'] == '':
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<i>Hi %s, before you can do any command you must enter your user id in the settings.py file to prevent strangers from sending commands to your PC!</i>\n\n<b>Here is your user ID:</b> <code>%s</code>" % (user['first_name'], user['id']))
        threading.Thread(target=shutdown, args=[context, update, "checkFailed"]).start()
        return False
    elif str(user['id']) != config['bot_settings']['user_id']:
        return False
    else:
        return True

def shutdown(context, update, reason):
    if reason == "cmd_stop":
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Bot turned off!")
    if reason == "checkFailed":
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="I am automatically turning off to allow you to make the change :)")

    updater.stop()
    updater.is_idle = False
    print("--------------------------------------")
    print("The bot has been shut down!")
    quit()

def processRunning(exe_name):
    r = os.popen('tasklist /v').read().strip().split('\n')
    for i in range(len(r)):
        if exe_name in r[i]:
            return True
    return False

updater = Updater(token=config['bot_settings']['token'], use_context=True)
dispatcher = updater.dispatcher

print("Bot online!")

def start(update, context):
    if checkUser(update, context) is True:
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Hello there :D")

def stop(update, context):
    if checkUser(update, context) is True:
        reason = "cmd_stop"
        threading.Thread(target=shutdown, args=(context, update, reason)).start()

def open(update, context):
    if checkUser(update, context) is True:
        file_name = ' '.join(context.args)
        file_name_c = file_name.capitalize()
        if file_name in config['paths']['files']:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Opening <b>%s</b>" % file_name_c)
            try:
                os.startfile(config['paths']['files'][file_name])
                context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> opened" % file_name_c)
                print("Opened %s" % file_name_c)
            except Exception:
                context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> has failed to open :(" % file_name_c)
                print("Failed to open %s" % file_name_c)
        else:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> is not defined in config.json" % file_name_c)
            print("Tried to open %s, but is not defined in config.json" % file_name_c)

def launch(update, context):
    if checkUser(update, context) is True:
        software_name = ' '.join(context.args)
        software_name_c = software_name.capitalize()
        if software_name in config['paths']['softwares']:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Launching <b>%s</b>" % software_name_c)
            try:
                os.startfile(config['paths']['softwares'][software_name])
                context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> launched :)" % software_name_c)
                print("Launched %s" % software_name_c)
            except Exception:
                context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> has failed to launch :(" % software_name_c)
                print("Failed to launch %s" % software_name_c)
        else:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> is not defined in config.json" % software_name_c)
            print("Tried to launch %s, but is not defined in config.json" % software_name_c)

def close(update, context):
    if checkUser(update, context) is True:
        name = ' '.join(context.args)
        if name in config['paths']['softwares']:
            name_c = name.capitalize()
            path = config['paths']['softwares'][name]
            path_split = path.split("\\")
            path_len = len(path_split)
            exe_name = path_split[path_len-1]
            if processRunning(exe_name) is True:
                context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Closing <b>%s</b>" % name_c)
                try:
                    exec("os.system('TASKKILL /F /IM %s')" % exe_name)
                    context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> closed :D" % name_c)
                except Exception:
                    context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> has failed to close" % name_c)
                    print("Failed to close %s" % name_c)
            else:
                context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> it is not open on the computer" % name_c)
        elif name in config['paths']['files']:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="This feature may come in the future, currently only the software can be closed :(")
        else:
            context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="<b>%s</b> is not defined in config.json" % name_c)
            print("Tried to close %s, but is not defined in config.json" % name_c)

def unknown(update, context):
    if checkUser(update, context) is True:
        context.bot.send_message(parse_mode="HTML", chat_id=update.effective_chat.id, text="Unkown command :(")

start_handler = CommandHandler('start', start)
stop_handler = CommandHandler('stop', stop)
open_handler = CommandHandler('open', open)
launch_handler = CommandHandler('launch', launch)
close_handler = CommandHandler('close', close)
unknown_handler = MessageHandler(Filters.text | Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(open_handler)
dispatcher.add_handler(launch_handler)
dispatcher.add_handler(close_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()