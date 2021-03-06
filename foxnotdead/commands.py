from peewee import *
from . import connection
from random import randint
from . import users
from . import states
from . import stats
from . import battle
from . import items as _items


class Command:
    def __init__(self, action, caption):
        pass


class UserStates(Model):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField(null=False)
    state_id = IntegerField(null=False)

    @classmethod
    def open(cls, user, state_id):
        user_state, created = cls.get_or_create(user_id=user.id, state_id=state_id)
        user_state.save()


class StateCommandNext(Model):
    id = PrimaryKeyField(null=False)
    command_id = IntegerField()
    state_id = IntegerField()
    prob = IntegerField()
    luck_based = BooleanField()

    @classmethod
    def get_next_state(cls, command):
        states = cls.select().where(cls.command_id == command.id)
        if len(states) == 1:
            return states.first().state_id

        total = 0
        prev = 0
        for _ in states: total += _.prob
        r = randint(0, total)
        for _ in states:
            if r > prev and x < _.prob:
                return _.state_id
            prev = _.prob

        return command.next_state_id

    class Meta:
        database = connection.db
        table_name = "state_command_next"


class StateCommand(Model):
    id = PrimaryKeyField(null=False)
    action = CharField()
    caption = CharField()
    state_id = IntegerField()
    next_state_id = IntegerField()
    requirement_container_id = IntegerField()
    reward_container_id = IntegerField()
    text = CharField()

    def execute(self, user):
        from .stats import UserStats, StatsHolder, UserStats
        from .loot import Container, ResourceContainer, ItemsContainer
        from .items import UserItems

        requirement_containter = Container.get_or_none(Container.id == self.requirement_container_id)

        if requirement_containter:
            unresolved_stats = UserStats.select() \
                .join(StatsHolder, on=(UserStats.stat_id == StatsHolder.stat_id)) \
                .where(StatsHolder.value > UserStats.value).count()
            print(unresolved_stats)
            if (unresolved_stats > 0):
                return "Чего-то тебе не хватает"

            uitems = UserItems.select().where(UserItems.user_id == user.id)
            for ritem in ItemsContainer.select().where(ItemsContainer.container_id == requirement_containter):
                for uitem in uitems:
                    if uitem.item_id == ritem.item_id:
                        if uitem.count < ritem.value:
                            uitem.count -= ritem.value
                            return "Чего-то тебе не хватает"

        reward_container = Container.get_or_none(Container.id == self.reward_container_id)
        if reward_container:
            reward_container.give_reward(user)
        """
        for uitem in uitems: uitem.save()
        for reward_item in ItemsContainer.select().where(ItemsContainer.container_id == reward_container):
            uitem, created = UserItems.get_or_create(item_id=reward_item.item_id, user_id=user.id)
            uitem.count = reward_item.value
            uitem.save()
        """
        user.set_state(
            StateCommandNext.get_next_state(self)
        )
        return "Готово!"

    class Meta:
        database = connection.db
        table_name = "state_command"


class BackCommand(Command):
    action = "b"
    caption = "Назад"

    @classmethod
    def execute(cls, user):
        user.state_id = user.prev_state_id
        user.prev_state_id = None
        user.save()
        return "готово"


class ViewInventory(Command):
    action = "u"
    caption = "Использовать предмет"

    @classmethod
    def execute(cls, user):
        user.set_state(states.UseItemState.db_id)
        return "Выбери предмет"


class InfoCommand(Command):
    action = "?"
    caption = "Посмотреть на себя"

    @classmethod
    def execute(cls, user):
        result = ()
        items = _items.UserItems.get_user_items(user.id)

        # print(user.stats.items())
        # exit(0)
        result += str(user.stats),
        result += "exp: " + str(user.exp),
        result += "level: " + str(user.level),

        # items = user.get_items()
        if not items:
            result += "У тебя нет ничего",
        else:
            result += "У тебя есть:",
            i = 0
            for _ in items:
                i += 1
                result += " " + str(i) + ")" + str(_.count) + " " + _.items.name ,
        return "\r\n".join(result)


class ShowItemsCommand(Command):
    action = "i"


class WalkCommand(Command):
    action = "w"
    caption = "Искать проблем на задницу"

    AGRESSIVE_SPOTTED = 0
    NOT_AGRESSIVE_SPOTTED = 1
    NOTHING_SPOTTED = 2

    @staticmethod
    def create_bot(user):
        return users.User.create_bot(user)

    @classmethod
    def execute(cls, user) -> str:
        # return msg , state, params, maybe
        x = randint(cls.AGRESSIVE_SPOTTED, cls.NOTHING_SPOTTED)
        if x == cls.NOT_AGRESSIVE_SPOTTED:  # if got troubles
            bot = cls.create_bot(user)
            battle.BattleData.start(user.id, bot.id)
            user.set_state(states.NotAgressiveSpottedState.db_id)
            return "Замечен враг: " + bot.name
        if x == cls.AGRESSIVE_SPOTTED:  # if got troubles
            bot = cls.create_bot(user)
            battle.BattleData.start(user.id, bot.id)
            user.set_state(states.AgressiveSpottedState.db_id)
            return "Замечен враг: Агрессивный " + bot.name
        else:
            return "Ничего не происходит"


""" we can make thios as graph"""


class RunCommand(Command):
    caption = "Смыться"

    @classmethod
    def execute(cls, user) -> str:
        have_run = randint(0, 1)
        if have_run:
            user.set_state(states.WalkState.db_id)
            battle.BattleData.finish(user)
            return "Ты смысля!"
        else:
            user.set_state(states.BattleState.db_id)
            return "Враг заметил тебя!"


class NewGameCommand(Command):
    caption = "Начать новую игру"

    @classmethod
    def execute(clsm, user) -> str:
        user.delete_everything()
        user.on_create()
        user.set_state(states.WalkState.db_id)
        return "Проснувшись рано утром, после беспокойного сна " + user.name + "обнаружил, что превратился в безобразного " \
                                                                               "ролевика. "


class AttackCommand(Command):
    caption = "Атаковать"

    @classmethod
    def execute(clsm, user) -> str:
        # create battle state
        # bot = users.User()
        bot = battle.UserBotMatch.get_bot(user)
        states.BattleState.Init(user, bot)
        user.set_state(states.BattleState.db_id)
        return ""


class KickCommand(Command):
    caption = "Пнуть врага"

    @staticmethod
    def get_loot(user, bot):

        pass

    @classmethod
    def execute(cls, user):
        result = ""
        user = user
        bot_id = battle.BattleData.get_enemy_id(user.id)
        bot = users.User.get_user(bot_id)

        damage = user.stats.damage + randint(-1, +20)
        bot.stats.health = bot.stats.health - damage

        result += "Ты пнул врага на " + str(damage) + ", " + str(bot.stats.health) + " здоровья осталось \r\n"
        if bot.stats.health <= 0:
            result += battle.BattleData.finish(user, bot, win=True)
            user.set_state(states.WinState.db_id)

        damage = bot.stats.damage + randint(-2, +2)
        result += "Враг пнул тебя на " + str(damage) + ", " + str(user.stats.health) + " здоровья осталось \r\n"
        user.stats.health -= damage
        if user.stats.health <= 0:
            result += "you win \r\n"
            result += battle.BattleData.finish(user, bot, win=False)
            user.set_state(states.DeathState.db_id)
        return result


class UseItemCommand(Command):
    @staticmethod
    def Init(id, name):
        return UseItemCommand(id, name)

    def __init__(self, id, name):
        self.item_id = id
        self.caption = "применить " + str(name)

    def execute(self, user):
        item_id = self.item_id
        item = _items.Items.get(_items.Items.id == self.item_id)

        result = item.name + " использовано.\r\n"
        item.get_user_item(user).use(user, item)
        user.state_id = user.prev_state_id
        user.prev_state_id = None
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
    caption = "Осмотреть врага"

    @classmethod
    def execute(cls, user):
        bot_id = battle.BattleData.get_enemy_id(user.id)
        bot = users.User.get_user(bot_id)
        result = ""
        result += bot.name + "\r\n"
        result += bot.get_info() + "\r\n"
        return result


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
