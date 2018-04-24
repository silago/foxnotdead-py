from random import randint
from . import users
from . import states
from . import battle
from . import items as _items


class Command:
    def __init__(self, action, caption):
        pass


class InfoCommand(Command):
    action = "?"
    caption = "get info about user"

    @classmethod
    def execute(cls, user):
        result = ""
        items = _items.UserItems.get_user_items(user.id)
        #items = user.get_items()
        for i in items:
            print(i)
        if not items:
            result = "you have nothing \r\n"
        else:
            result = "you have something \r\n"
        return result





class ShowItemsCommand(Command):
    action = "i"

class WalkCommand(Command):
    action = "w"
    caption = "look for troubles"

    AGRESSIVE_SPOTTED = 0
    NOT_AGRESSIVE_SPOTTED = 1
    NOTHING_SPOTTED = 2

    @staticmethod
    def create_bot():
        return users.User.create_bot()

    @classmethod
    def execute(cls, user) -> str:
        # return msg , state, params, maybe
        x = randint(cls.AGRESSIVE_SPOTTED, cls.NOTHING_SPOTTED)
        if x == cls.NOT_AGRESSIVE_SPOTTED:  # if got troubles
            bot = cls.create_bot()
            battle.BattleData.start(user.id, bot.id)
            user.set_state(states.NotAgressiveSpottedState)
            return "friendly man spotted"
        if x == cls.AGRESSIVE_SPOTTED:  # if got troubles
            bot = cls.create_bot()
            battle.BattleData.start(user.id, bot.id)
            user.set_state(states.AgressiveSpottedState)
            return "agressive enemy spotted"
        else:
            return "nothing happens"


""" we can make thios as graph"""


class RunCommand(Command):
    caption = "Leave"

    @classmethod
    def execute(cls, user) -> str:
        have_run = randint(0, 1)
        if have_run:
            user.set_state(states.WalkState)
            battle.BattleData.finish(users.id)
            return "you've runned"
        else:
            user.set_state(states.BattleState)
            return "you couldn't run. defend yourseld"


class AttackCommand(Command):
    caption = "Attack"

    @classmethod
    def execute(clsm, user) -> str:
        # create battle state
        bot = users.User()
        states.BattleState.Init(user, bot)
        user.set_state(states.BattleState)
        return "You attack"


class KickCommand(Command):
    caption = "Kick enemy"

    @classmethod
    def execute(cls, user):
        result = ""

        user = user
        bot = users.User.get_user(user.state_param)
        damage = user.damage + randint(-2, +2)
        bot.health -= damage
        result += "you've kicked enemy at " + str(damage) + ", " + str(bot.health) + " health left \r\n"
        if bot.health <= 0:
            battle.BattleData.finish(users.id)
            user.set_state(states.WinState)

        damage = bot.damage + randint(-2, +2)
        result += "you've kicked enemy at " + str(damage) + ", " + str(user.health) + " health left"
        user.health -= damage
        if user.health <= 0:
            battle.BattleData.finish(users.id)
            user.set_state(states.DeathState)
        return result

class InspectEnemyCommand(Command):
    caption = "Inspect enemy"

    @classmethod
    def execute(cls, user):
        bot_id = battle.BattleData.get_enemy_id(user.id)
        bot = users.User.get_user(bot_id)
        return bot.get_info()


"""
    state or command struct
    name 
    caption
    id
    ....
    ....
    bool reserved
"""

def GetParamActionCommands():
    pass


class ParamCommand(Command):
    item_requirement = []
    item_rewards = []
    stats_requirement = []
    stats_rewards = []

    @classmethod
    def Create(cls, action, caption):
        command = ParamCommand(action, caption)
        return command
        pass

    def __init__(self, action, caption):
        self.action = action
        self.caption = caption

    def execute(self):
        pass

    pass
