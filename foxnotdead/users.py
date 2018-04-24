from .import  states
from peewee import *
import application.foxnotdead.connection as connection
from . import items
from . import stats

class User(Model):
    id = PrimaryKeyField(null=False)
    name      = CharField()
    state_id  = IntegerField()

    id = 0
    is_bot = False
    location = 0
    battle_id = 0
    health = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Level = 1
        self.damage = 10
        self.health = 100
        self._stats = self._get_stats()


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

    def _get_stats(self):

        result = {}
        stats_keys = stats.Stats.all()
        stats_vals =  stats.UserStats.select().wheres(stats.UserStats.user_id == self.id)

        for _ in stats_keys:
            for s in stats_vals:
                if s.stat_id == _.id:
                    result[_.key]=s.value

        return result


    def _compute_stat(self, stat_id):
        # compute stats:
        # 1. compute user class level stats
        # 2. compute user items stats
        # 3 ???
        return 100
        pass

    def _compute_stats(self):
       stats_keys = stats.Stats.all()
       result = {}
       for stats_key in stats_keys:
           result[stats_keys.key] = self._compute_stat(stats_keys.id)
           stat = stats.UserStats.get_or_create(stats.UserStats.user_id == self.id, stats.UserStats.stat_id == stats_key.stat_id)
           stat.value = result[stats_keys.key]
           stat.save()
       self._stats = result


    def get_damage(self):
        pass


    def get_info(self):
        return "It's some bot"

    @staticmethod
    def get_user(id) -> object:
        return User.create_base()

    @staticmethod
    def create_base():
        user = User()
        user.Name = "Silago"
        user.Class = None
        user.Level = 1
        user.damage = 10
        user.health = 100
        return user

    def get_state(self):
        return states.BaseState.get_state(self.state_id)

    def set_state(self, state, state_param = None):
        print("SET STATE")
        self.state_id = state.db_id
        #self.state_param = state_param
        self.save()

    def get_items(self):
        return items.UserItems.get_user_items(self.id)

    @staticmethod
    def create_bot():
        bot = User()
        bot.name = "Bot"
        #bot.Class = None
        #bot.Level = 1
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

