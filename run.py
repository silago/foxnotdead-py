import sys, os
from foxnotdead import models

from foxnotdead import items
from foxnotdead import users

from peewee import *




class App:
    @staticmethod
    def run() -> None:
        #user = users.User.get_user(1)
        while True:
            user = users.User.get(users.User.name == 'silago')
            state = user.get_state()
            commands = state.get_commands(user)
            print("current state: "+ state.get_caption())
            for _ in commands:
                print(_ + " " + commands[_].caption)

            user_input = input()#input("enter the command \r\n")
            data = state.process_input(user, user_input)
            print(data)
            #afteward print state actions
App.run()


