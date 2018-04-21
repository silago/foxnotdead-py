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



    @staticmethod
    def get_user(id) -> object:
        return User.create_base()

    @staticmethod
    def create_base():
        user = User()
        user.Name = "Silago"
        user.Class = None
        user.Level = 1
        user.StateID = 1
        user.damage = 10
        user.health = 100
        return user

    def get_state(self):
        return states.BaseState.get_state(self.state_id)

    def set_state(self, state, state_param = None):
        print("SET STATE")
        self.state = state
        self.StateID = state.id
        print(self.StateID)
        self.state_param = state_param
        self.state_id = state.id
        print(self.state_id)
        self.save()
        pass

    def get_items(self):
        return items.UserItems.get_user_items(self.id)

    @staticmethod
    def create_bot():
        bot = User()
        bot.is_bot = True
        bot.id = 11
        bot.Name = "Bot"
        bot.Class = None
        bot.Level = 1
        bot.State = 0
        return bot

    class Meta:
        database = connection.db
        table_name = "users"

