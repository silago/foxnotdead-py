from random import randint
from . import users
from . import states
from . import stats
from . import battle
from . import items as _items


class Command:
    def __init__(self, action, caption):
        pass


class BackCommand(Command):
    action = "b"
    caption = "go back"

    @classmethod
    def execute(cls, user):
        user.state_id = user.prev_state_id
        user.prev_state_id = None
        user.save()
        return "return"

class ViewInventory(Command):
    action = "u"
    caption = "use item"

    @classmethod
    def execute(cls, user):
        user.set_state(states.UseItemState)
        return "Choose item to use"


class InfoCommand(Command):
    action = "?"
    caption = "get info about user"

    @classmethod
    def execute(cls, user):
        result = ""
        items = _items.UserItems.get_user_items(user.id)
        stats = user.get_stats()

        # items = user.get_items()
        if not items:
            result = "you have nothing \r\n"
        else:
            result = "you have: \r\n"
            i = 0
            for _ in items:
                i += 1
                result += " " + str(i) + ")" + str(_.count) + " " + _.items.name + "\r\n"
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
        bot_id = battle.BattleData.get_enemy_id(user.id)
        bot = users.User.get_user(bot_id)
        damage = user.damage + randint(-2, +2)
        bot.health -= damage
        result += "you've kicked enemy at " + str(damage) + ", " + str(bot.health) + " health left \r\n"
        if bot.health <= 0:
            battle.BattleData.finish(users.id)
            user.set_state(states.WinState)

        damage = bot.damage + randint(-2, +2)
        result += "enemy kicked you at " + str(damage) + ", " + str(user.health) + " health left"
        user.health -= damage
        if user.health <= 0:
            battle.BattleData.finish(user.id)
            user.set_state(states.DeathState)
        return result


class UseItemCommand(Command):
    @staticmethod
    def Init(id,name):
        return UseItemCommand(id, name)

    def __init__(self, id, name):
        self.item_id = id
        self.caption = "use item " + str(name)

    def execute(self, user):
        item_id = self.item_id
        item = _items.Items.get(_items.Items.id == item_id)
        result = "ypu are using " + item.name + "\r\n"

        ui = _items.UserItems.get(_items.UserItems.item_id == item_id, _items.UserItems.user_id == user.id)
        ui.count -= 1

        item_stats = _items.ItemsStats.select().where(_items.ItemsStats.item_id == item_id)
        user_stats = stats.UserStats.select().where(stats.UserStats.user_id == user.id)
        for item_stat in item_stats:
            for user_stat in user_stats:
                if (user_stat.stat_id == item_stat.stat_id):
                    user_stat.value += item_stat.value
                    user_stat.save()
                    result += "stat " + str(user_stat.stat_id) + "+= " + str(user_stat.value)
        result += "\r\n"
        result += str(ui.count) + " " + item.name + " left"
        user.prev_state_id = None
        user.state_id = user.prev_state_id
        user.save()

        return result


"""
class UseItemCommand(Command):
    captiom = "use item"
    @classmethod
    def execute(cls, user, id):
        bot_id = battle.BattleData.get_enemy_id(user.id)
        bot = users.User.get_user(bot_id)
        return bot.get_info()

class ShowInventory(Command):
    caption = "Show inventory "
    @classmethod
    def execute(cls, user):
        result = ""
        items = _items.UserItems.get_user_items(user.id)
        if not items:
            result = "you have nothing \r\n"
        else:
            result = "you have: \r\n"
            i = 0
            for _ in items:
                i+=1
                result += " "+str(i)+")" + str(_.count) + " " + _.items.name + "\r\n"
        return result
"""


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
