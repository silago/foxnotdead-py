from .import  states
from peewee import *
import application.foxnotdead.connection as connection
from . import items

class User(Model):
    id = PrimaryKeyField(null=False)
    name      = CharField()
    state_id  = IntegerField()

    id = 0
    is_bot = False
    location = 0
    battle_id = 0
    health = 50


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

