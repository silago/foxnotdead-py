import sys, os
import foxnotdead.users as users
import foxnotdead.connection as connection


from peewee import *



class App:
    @staticmethod
    def run() -> None:
        #user = users.User.get_user(1)
        print(users)
        exit(0)
        user = users.User.get(users.User.name == 'silago')
        while True:
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


