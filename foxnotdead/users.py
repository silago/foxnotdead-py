from peewee import *

import foxnotdead.states as states
import foxnotdead.stats  as stats

from . import connection


class BotTemplate(Model):
    id = PrimaryKeyField(null=False)
    reward_container_id = IntegerField()
    level_id = IntegerField()

    class Meta:
        database = connection.db
        table_name = "bot_templates"


class User(Model):
    id = PrimaryKeyField(null=False)
    name = CharField()
    state_id = IntegerField()
    prev_state_id = IntegerField()
    level = IntegerField()
    exp = IntegerField()
    is_bot = BooleanField()
    related_name = "User"

    def __unicode__(self):
        return self.name

    def Init(self):
        from .levels import Levels
        if not self.level: self.level = 1
        if not self.exp: self.exp = 1
        if not self.state_id: self.state_id = 1

        level = Levels.get(Levels.id == self.level)
        print("3>>>")
        print(self.id)
        self.damage = 10
        self.health = 100
        self._compute_stats()

        print("4>>>")

        if not self.is_bot:
            if level.exp < self.exp:
                # while level.exp < self.exp:
                #    self.level += 1
                self.level += 1

                self._compute_stats()
                self.save()

        print("5>>>")
        self._stats = self._get_stats()
        print("6>>>")
        pass

    def __init__(self, *args, **kwargs):
        from .levels import Levels
        super().__init__(*args, **kwargs)
        self.health = 100
        self.damage = 10
        print("1>>>")
        print("2>>>")

    def on_equip_(self):
        pass

    def on_dequip_(self):
        pass

    def update_stats(self):
        # get level stats
        # get equipped items stats
        pass

    def get_stats(self):
        return self._stats

    def get_stat(self, name):
        return self._stats(name)

    def _get_stats(self):
        from .stats import Stats, UserStats
        user_stats = UserStats \
            .select(UserStats.stat_id, UserStats.value, Stats.name) \
            .join(Stats, on=(UserStats.stat_id == Stats.id)) \
            .where(UserStats.user_id == self.id)
        result = {_.stats.name: _.value for _ in user_stats}
        return result

    def _compute_stat(self, stat_id):
        from .loot import Container
        from .levels import ClassLevelStats
        from .stats import StatsHolder

        from .items import ItemsStats, UserItems, Items

        level_stat = StatsHolder.select(StatsHolder.value) \
            .join(ClassLevelStats, on=(StatsHolder.container_id == ClassLevelStats.container_id)) \
            .where(
            StatsHolder.stat_id == stat_id,
        ).first()
        lvval = level_stat.value if level_stat else 0

        items_stat = UserItems.select(fn.COALESCE(fn.SUM(ItemsStats.value), 0).alias('total')) \
            .join(Items, on=(Items.id == UserItems.id)) \
            .join(ItemsStats, on=(ItemsStats.item_id == Items.id)) \
            .where(
            UserItems.user_id == self.id,
            UserItems.slot_id,
            Items.equipable,
            ItemsStats.stat_id == stat_id
        ).first()

        itemval = items_stat.total

        return lvval + itemval

    def _compute_stats(self):
        from .stats import Stats, UserStats
        stats_keys = Stats.select().where(True)
        result = {}
        for stats_key in stats_keys:
            result[stats_key.key] = self._compute_stat(stats_key.id)
            stat, created = stats.UserStats.get_or_create(user_id=self.id,
                                                          stat_id=stats_key.id)
            stat.value = int(result[stats_key.key])
            stat.save()
        self._stats = result

    def get_damage(self):
        pass

    def get_info(self):
        return "It's some bot"

    @staticmethod
    def get_user(user_id) -> object:
        if user_id:
            return User.get(User.id == user_id)
        else:
            return User.create_base()

    @staticmethod
    def create_base():
        user = User()
        user.Name = "Silago"
        user.Class = None
        user.Level = 1
        # user.damage = 10
        # user.health = 100

        return user

    def get_state(self):
        return states.BaseState.get_state(self.state_id)

    def set_state(self, state, state_param=None):
        self.prev_state_id = self.state_id
        self.state_id = state.db_id

        # self.state_param = state_param
        self.save()

    def get_items(self):
        import foxnnotdead.items as items
        return items.UserItems.get_user_items(self.id)

    @staticmethod
    def create_bot(user):
        from .battle import UserBotMatch
        bot = UserBotMatch.get_bot(user)
        return bot
        bot = User()
        bot.name = "Bot"
        bot.is_bot = 1
        bot.save()

        return bot


    class Meta:
        database = connection.db
        table_name = "users"


class Levels(Model):
    pass


class Class(Model):
    pass


class UserClass(Model):
    pass


class ClassLevelStats(Model):
    pass
