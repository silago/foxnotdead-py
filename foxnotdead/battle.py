from peewee import *
import application.foxnotdead.connection as connection
from . import users
from . import items
from . import loot

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
        battle = BattleData()
        battle.user_id = user_id
        battle.enemy_id = bot_id
        battle.save()

    @classmethod
    def finish(cls, user, bot, win):
        BattleData.delete().where(BattleData.user_id == user.id).execute()
        result = ""
        if win:
            result = loot.get_bot_loot(user, bot)
        #bot.delete().execute()
        return  result

    class Meta:
        database = connection.db
        table_name = "battle_data"
