import sys, os
from foxnotdead import models

from foxnotdead import items
from foxnotdead import users

from peewee import *


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#print(os.environ['tg_token'])
updater = Updater(os.environ['tg_token'])


import logging

#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)


class App:
    @staticmethod
    def cycle(bot, update):
        txt = ""
        user, created = users.User.get_or_create(name=update.message.from_user.first_name)
        if created:
            user.on_create()
        if created:
            user.save()
        user.Init()

        state = user.get_state()
        # commands = state.get_commands(user)

        user_input = update.message.text
        txt = str(state.process_input(user, user_input)) + "\r\n"

        state = user.get_state()
        commands = state.get_commands(user)
        txt += "" + str(state.get_caption()) + "\r\n"
        for _ in commands:
            txt += str(_) + " " + str(commands[_].caption) + "\r\n"


        result = "--------------\r\n"
        result += txt
        result += "--------------\r\n"
        update.message.reply_text(txt)

    @staticmethod
    def run(name) -> None:
        # user = users.User.get_user(1)
        while True:
            user, created      = users.User.get_or_create(name=name)

            if created:
                user.save()
                user.on_create()

            user.Init()
            state = user.get_state()
            print(state.get_caption())
            print(
                "\r\n".join([k+": "+v.caption for k,v in user.get_state().get_commands(user).items()])
            )

            user_input = input()  # input("enter the command \r\n")
            data = state.process_input(user, user_input)
            print("-----------")
            print(data)
            print("-----------")


import sys

if sys.argv[1] == "tg":
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, App.cycle))
    updater.start_polling()
    updater.idle()
else:
    App.run(sys.argv[1])
