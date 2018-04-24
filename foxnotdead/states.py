from . import commands
from peewee import *
import application.foxnotdead.connection as connection

class BaseState(Model):
    id = PrimaryKeyField(null=False)
    db_id = 0
    commands = {
        "i" : commands.InfoCommand,
        "u1" : commands.UseItemCommand.Init(1),
        "u2" : commands.UseItemCommand.Init(2),
        "u3" : commands.UseItemCommand.Init(3),
        "u4" : commands.UseItemCommand.Init(4),
        "u5" : commands.UseItemCommand.Init(5),
        "u6" : commands.UseItemCommand.Init(6),
        "u7" : commands.UseItemCommand.Init(7),
        "u8" : commands.UseItemCommand.Init(8)
    }
    caption = "no state description"

    def get_caption(self):
        return self.caption

    @staticmethod
    def get_states():
        return {_.db_id: _ for _ in (
            WalkState, AgressiveSpottedState, NotAgressiveSpottedState, BattleState, InitState, DeathState, WinState
        )}

    @classmethod
    def get_state(cls, id): # from db and bind it
        print("find state # " + str(id))
        dbstate = BaseState.get(BaseState.id == id)
        return dbstate._as(cls.get_states().get(dbstate.id,dbstate))

    def process_input(self, user, input: str):
        commands = self.get_commands()
        command = commands.get(input)
        if (command):
            result = command.execute(user)
            return result
        else:
            return None

    def _as(self, _class):
        self.__class__ = _class
        return self


    @classmethod
    def get_id(cls):
        return cls.db_id

    @classmethod
    def get_self(cls):
        print()
        pass


    def get_commands(self):
        base_commands = BaseState.commands
        return {**base_commands, **self.commands}

    class Meta:
        database = connection.db
        table_name = "states"


class WalkState(BaseState):
    caption = "you are walking"
    db_id = 1
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


    db_id = 2
    commands = {
        "k": commands.KickCommand,
        "e": commands.InspectEnemyCommand,
    }


class NotAgressiveSpottedState(BaseState):
    caption = "not agressive enemy spotted "
    db_id = 3
    commands = {
        "r": commands.RunCommand,
        "a": commands.AttackCommand,
    }


class AgressiveSpottedState(BaseState):
    caption = "agressive enemy spotted "
    db_id = 4
    commands = {
        "r": commands.RunCommand,
        "a": commands.AttackCommand,
        "e": commands.InspectEnemyCommand,
    }


class InitState(BaseState):
    db_id = 5


class DeathState(BaseState):
    caption = "you dead"
    db_id = 6
    commands = {
        "*": InitState,
        "w": commands.WalkCommand
    }
    pass


class WinState(BaseState):
    caption = "you win"
    db_id = 7
    commands = {
        "*": WalkState
    }

    def process_input(self, User, input: str):
        User.Win()
        return super().process_input(User, input)
