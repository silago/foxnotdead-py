import sys, os
from foxnotdead import models

from foxnotdead import items
from foxnotdead import users

from peewee import *

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater('590889402:AAG-OPeK9bJAPdNU_9h_WXYs7e8eLfZBy7E')

import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)


class App:
    @staticmethod
    def cycle(bot, update):
        txt = ""
        user, created = users.User.get_or_create(name=update.message.from_user.first_name)
        if created:
            print(user)
            user.save()
        print("<<<<<<<<<<")
        user.Init()

        state = user.get_state()
        # commands = state.get_commands(user)

        user_input = update.message.text
        txt = str(state.process_input(user, user_input)) + "\r\n"

        state = user.get_state()
        commands = state.get_commands(user)
        txt += "current state: " + str(state.get_caption()) + "\r\n"
        for _ in commands:
            txt += str(_) + " " + str(commands[_].caption) + "\r\n"

        print(txt)
        update.message.reply_text(txt)

    @staticmethod
    def run(name) -> None:
        # user = users.User.get_user(1)
        while True:
            print(">>>>>>>>>")
            user, created      = users.User.get_or_create(name=name)

            if created:
                print(user)
                user.save()
            print("<<<<<<<<<<")
            user.Init()

            state = user.get_state()
            commands = state.get_commands(user)
            print("current state: " + state.get_caption())
            for _ in commands:
                print(_ + " " + commands[_].caption)

            user_input = input()  # input("enter the command \r\n")
            data = state.process_input(user, user_input)
            print(data)
            # afteward print state actions


import sys

if sys.argv[1] == "tg":
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, App.cycle))
    updater.start_polling()
    updater.idle()
else:
    App.run(sys.argv[1])
