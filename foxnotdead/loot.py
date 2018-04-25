from . import states
from peewee import *
import application.foxnotdead.connection as connection
from . import items
from . import stats




class BotRewardContainer(Model):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField()
    container_id = IntegerField()

    @classmethod
    def create_default_loot(cls, bot):
        # experiance = sta id ?
        # bear = item_id ?
        container = Container()
        container.save()
        bot_reward_container = BotRewardContainer()

        bot_reward_container.user_id = bot.id
        bot_reward_container.container_id = container.id
        bot_reward_container.save()

        items_container = ItemsContainer()
        items_container.item_id =

class Container(Model):
    id = PrimaryKeyField(null=False)

class ResourceContainer(Model):
    id = PrimaryKeyField(null=False)

class ItemsContainer(Model):
    id = PrimaryKeyField(null=False)
    container_id = IntegerField()
    item_id  = IntegerField()
    value    = IntegerField()

class StatsContainer(Model):
    id = PrimaryKeyField(null=False)
    stat_id = IntegerField()
    item_id  = IntegerField()
    value    = IntegerField()
