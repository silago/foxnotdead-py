from . import commands
from . import items
from peewee import *
import application.foxnotdead.connection as connection

class BaseState(Model):
    id = PrimaryKeyField(null=False)
    db_id = 0
    commands = {
        "i" : commands.InfoCommand,
        "u" : commands.ViewInventory,
    }
    caption = "no state description"

    def get_caption(self):
        return self.caption

    @staticmethod
    def get_states():
        return {_.db_id: _ for _ in (
            WalkState, AgressiveSpottedState, NotAgressiveSpottedState, BattleState, InitState, DeathState, WinState, UseItemState
        )}

    @classmethod
    def get_state(cls, id): # from db and bind it
        print("find state # " + str(id))
        dbstate = BaseState.get(BaseState.id == id)
        return dbstate._as(cls.get_states().get(dbstate.id,dbstate))

    def process_input(self, user, input: str):
        commands = self.get_commands(user)
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
        pass


    def get_commands(self, user):
        base_commands = BaseState.commands
        return {**base_commands, **self.commands}

    class Meta:
        database = connection.db
        table_name = "states"

class UseItemState(BaseState):
    caption = "Choose item"
    db_id = 8
    commands = {
        "b" : commands.BackCommand
    }

    def get_commands(self, user):
        user_items = items.UserItems.get_user_items(user.id)
        _commands = {}
        counter= 0
        for _ in user_items:
            _commands[str(counter)] = commands.UseItemCommand.Init(_.items.id, _.items.name)
        base_commands = BaseState.commands
        return {**base_commands, **UseItemState.commands, **_commands}



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
    caption = "you win commands"
    db_id = 7
    commands = {
        "*": WalkState
    }

    def process_input(self, _user, input: str):
        return commands.WalkCommand.execute(_user)
        #return super().process_input(User, input)
