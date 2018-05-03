from peewee import *
from . import connection
from . import users
from . import items
from . import loot



class UserBotMatch():
    @staticmethod
    def get_bot(user):
        from .users import  User
        bot = User.select().where(User.is_bot == True, User.id != user.id, User.level<user.level+2, User.level>user.level-2).order_by(fn.Random()).limit(1).first()
        bot.Init()
        return bot

class BattleData(Model):
    id = PrimaryKeyField(null=False)
    user_id  = IntegerField()
    enemy_id = IntegerField()

    @classmethod
    def get_enemy_id(cls, user_id):
        user = cls.get(BattleData.user_id == user_id)
        return user.enemy_id

    @classmethod
    def start(cls, user_id, bot_id):
        from . import users
        battle = BattleData()
        battle.user_id = user_id
        battle.enemy_id = bot_id
        bot = users.User.get(users.User.id == bot_id)
        bot.on_create()
        battle.save()

    @classmethod
    def finish(cls, user, bot=None, win=False):
        BattleData.delete().where(BattleData.user_id == user.id).execute()
        result = ""
        if win:
            result+= loot.get_bot_loot(user, bot)
            result+str(bot.exp) + " Опыта получено"
            user.exp += bot.exp
            user.save()
        return  result

    class Meta:
        database = connection.db
        table_name = "battle_data"
