from . import commands
from peewee import *
import application.foxnotdead.connection as connection

class BaseState(Model):
    id = PrimaryKeyField(null=False)
    commands = {
        "i" : commands.InfoCommand
    }
    caption = "no state description"

    #def __init__(self, user):
    #    self.User = user

    def get_caption(self):
        return self.caption

    @staticmethod
    def get_states():
        return {_.id: _ for _ in (
            WalkState, AgressiveSpottedState, NotAgressiveSpottedState, BattleState, InitState, DeathState, WinState
        )}

    @classmethod
    def get_state(cls, id):
        try:
            state = BaseState.get(BaseState.id == id)
        except Exception as e:
            print("colud not get state from db.")
            print(e)

        return state

    def process_input(self, user, input: str):
        commands = self.get_commands()
        command = commands.get(input)
        if (command):
            result = command.execute(user)
            return result
        else:
            return None


    def get_commands(self):
        base_commands = BaseState.commands
        return {**base_commands, **self.commands}

    class Meta:
        database = connection.db
        table_name = "states"


class WalkState(BaseState):
    caption = "you are walking"
    id = 1
    commands = {
        "w": commands.WalkCommand
    }


class BattleState(BaseState):
    caption = "you are in battle"
    class BattleBotState:
        id = 0
        state_id = 0
        bot_id = 0

    @classmethod
    def Init(cls, user, bot):
        pass


    id = 2
    commands = {
        "k": commands.KickCommand
    }


class NotAgressiveSpottedState(BaseState):
    caption = "not agressive enemy spotted "
    id = 3
    commands = {
        "r": commands.RunCommand,
        "a": commands.AttackCommand,
    }


class AgressiveSpottedState(BaseState):
    caption = "agressive enemy spotted "
    id = 4
    commands = {
        "r": commands.RunCommand,
        "a": commands.AttackCommand,
    }


class InitState(BaseState):
    id = 5


class DeathState(BaseState):
    caption = "you dead"
    id = 6
    commands = {
        "*": InitState
    }
    pass


class WinState(BaseState):
    caption = "you win"
    id = 7
    commands = {
        "*": WalkState
    }

    def process_input(self, User, input: str):
        User.Win()
        return super().process_input(User, input)
