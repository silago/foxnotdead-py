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

    class UserStatsContainer:
        _ignore_computing = "chealth",

        def __init__(self, user):
            from .stats import Stats, UserStats
            self._binds = {
                "health": "chealth"
            }
            self._stats_keys = {_.key: _ for _ in Stats.select().where(True)}
            self._user = user
            # self._stats = self._compute_stats()
            self._stats = {_.key: _.userstats.value for _ in Stats.select(Stats, UserStats.value).join(UserStats, on=(
                    Stats.id == UserStats.stat_id)).where(UserStats.user_id == user.id)}

        def __getattr__(self, item):
            item = self._binds.get(item, item)
            return self._stats.get(item)

        def __setattr__(self, key, value):
            from .stats import Stats, UserStats
            # do not use st attr at protected methods
            if key[0] == "_":
                self.__dict__[key] = value
                return

            key = self._binds.get(key, key)

            self._stats[key] = value
            stat_id = self._stats_keys[key]
            stat, created = UserStats.get_or_create(user_id=self._user.id,
                                                    stat_id=stat_id)
            stat.value = value if value else 0
            stat.save()

        def __str__(self):
            return "\r\n".join([key + ": " + str(value) for key, value in self._stats.items()])

        def __unicode__(self):
            return str(self._stats)

        def by_id(self, id):
            for _, v in self._stats_keys.items():
                if v.id == id: return _

        def set_by_id(self, id, value):
            key = None
            for _, v in self._stats_keys.items():
                if v.id == id:
                    key = _
            self.__setattr__(key, value)


        def items(self):
            return self._stats.items()

        def _compute_stat(self, stat_id):
            if (stat_id == 4):
                print("COMPUTE HEALTH")
                exit(0)
            from .loot import Container
            from .levels import ClassLevelStats
            from .stats import StatsHolder

            from .items import ItemsStats, UserItems, Items

            level_stat = StatsHolder.select(StatsHolder.value) \
                .join(ClassLevelStats, on=(StatsHolder.container_id == ClassLevelStats.container_id)) \
                .where(
                StatsHolder.stat_id == stat_id,
            ).first()
            level_stat_value = level_stat.value if level_stat else 0
            if not level_stat_value: level_stat_value = 0
            items_stat = UserItems.select(fn.COALESCE(fn.SUM(ItemsStats.value), 0).alias('total')) \
                .join(Items, on=(Items.id == UserItems.id)) \
                .join(ItemsStats, on=(ItemsStats.item_id == Items.id)) \
                .where(
                UserItems.user_id == self._user.id,
                UserItems.slot_id != None,
                Items.equipable == True,
                ItemsStats.stat_id == stat_id
            ).first()

            item_stat_value = items_stat.total if items_stat.total else 0

            return level_stat_value + item_stat_value

        # TODO:: call this only on init or stats changed
        def _compute_stats(self):
            from .stats import Stats, UserStats
            result = {}
            for stat_key, stat_value in self._stats_keys.items():
                if stat_key not in User.UserStatsContainer._ignore_computing:
                    result[stat_key] = self._compute_stat(stat_value.id)
                else:
                    result[stat_key] = 0
                stat, created = UserStats.get_or_create(user_id=self._user.id,
                                                        stat_id=stat_value.id)
                stat.value = int(result[stat_key])
                stat.save()
            return result

        def _get_stats(self):
            from .stats import Stats, UserStats
            user_stats = UserStats \
                .select(UserStats.stat_id, UserStats.value, Stats.name) \
                .join(Stats, on=(UserStats.stat_id == Stats.id)) \
                .where(UserStats.user_id == self.id)
            result = {_.stats.name: _.value for _ in user_stats}
            return result

    def Init(self):
        from .levels import Levels
        if not self.level: self.level = 1
        if not self.exp: self.exp = 1
        if not self.state_id: self.state_id = 1

        level = Levels.get(Levels.id == self.level)
        # self.damage = 10
        # self.health = 100
        # self.stats = Stats(self._compute_stats())w

        if not self.is_bot:
            if level.exp < self.exp:
                self.level += 1
                self.save()

        # self._stats = self._get_stats()
        pass

    def delete_everything(self):
        from . import items
        items.UserItems.delete().where(items.UserItems.user_id == self.id).execute()

    def on_create(self):
        # 1. set tutorial (intro state)
        # 2. set current health = max_health
        self.stats._compute_stats()
        self.stats.health = self.stats.mhealth

        pass

    def __init__(self, *args, **kwargs):
        from .levels import Levels
        super().__init__(*args, **kwargs)
        # self.health = 100
        # self.damage = 10
        self.stats = self.UserStatsContainer(self)

    def on_equip_(self):
        pass

    def on_dequip_(self):
        pass

    def update_stats(self):
        pass

    # def get_stats(self):
    #    return self.stats

    # def get_stat(self, name):
    #    return self._stats(name)

    def get_damage(self):
        pass

    def get_info(self):
        return str(self.stats)

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

    def set_state(self, state_id, state_param=None):
        from .states import UserStates, BaseState
        user_state, created = UserStates.get_or_create(
            user_id=self.id, state_id=state_id
        )
        if created: user_state.save()

        self.prev_state_id = self.state_id
        self.state_id = state_id
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
