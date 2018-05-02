from . import states
from peewee import *
from . import connection
from . import items
from . import stats
from . import users

"""

def get_bot_loot(user, bot):
    result = '"'
    try:
        bot_reward_container = BotRewardContainer.get(BotRewardContainer.user_id == bot.id)
    except:
        return "You've recieve nothing"
    container =  Container.get(Container.id == bot_reward_container.container_id)
    item_containers = ItemsContainer.select().where(ItemsContainer.container_id == container.id)
    for item_container in item_containers:
        item = items.Items.get(items.Items.id == item_container.item_id)
        user_item, created = items.UserItems.get_or_create( item_id = item_container.item_id, user_id = user.id)
        if not user_item.count:
            user_item.count = 0
        user_item.count += item_container.value
        user_item.save()
        result += "You get  "+str(user_item.count)+ " "+item.name+"\r\n"

    return result
"""


def get_bot_loot(user, bot):
    result = '"'
    try:
        bot_reward_container = BotRewardContainer.get(BotRewardContainer.user_id == bot.id)
        container = Container.get(Container.id == bot_reward_container.container_id)
        return container.give_reward(user)
    except Exception as e:
        print(e)
        return "You've recieve nothing"
    # user = users.User.get(users.User.name == 'silago')


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
        items_container.item_id = 1  # it's bear
        items_container.value = 5

    class Meta:
        database = connection.db
        table_name = "bot_reward_container"


class Container(Model):
    id = PrimaryKeyField(null=False)

    class Meta:
        database = connection.db
        table_name = "container"

    def get_restriction(self):
        pass

    def give_reward(self, user):
        from .items import UserItems
        for reward_item in ItemsContainer.select().where(ItemsContainer.container_id == self.id):
            uitem, created = UserItems.get_or_create(item_id=reward_item.item_id, user_id=user.id)
            uitem.count = reward_item.value
            uitem.save()

        for reward in CommandReward.select().where(CommandReward.container_id == self.id):
            command, created = UserCommand.get_or_create(item_id=reward.item_id, user_id=user.id)
            if created:
                command.save()

        for reward in StatsContainer.select().where(StatsContainer.container_id == self.id):
            user.stats.set_by_id(reward.value)

        return "You got something"


class ResourceContainer(Model):
    id = PrimaryKeyField(null=False)

    class Meta:
        database = connection.db
        table_name = "resource_container"


class ItemsContainer(Model):
    id = PrimaryKeyField(null=False)
    container_id = IntegerField()
    item_id = IntegerField()
    value = IntegerField()

    class Meta:
        database = connection.db
        table_name = "items_container"


class StatsContainer(Model):
    id = PrimaryKeyField(null=False)
    stat_id = IntegerField()
    item_id = IntegerField()
    value = IntegerField()

    class Meta:
        database = connection.db
        table_name = "stats_container"


class CommandReward(Model):
    id = PrimaryKeyField(null=False)
    container_id = IntegerField()
    command_id = IntegerField()

    class Meta:
        database = connection.db
        table_name = "command_reward"


class UserCommand(Model):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField()
    command_id = IntegerField()

    class Meta:
        database = connection.db
        table_name = "user_commands"
