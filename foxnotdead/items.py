from peewee import *
import application.foxnotdead.connection as connection

"""
class Stats:
    def __init__(self,id, name):
        pass
    @staticmethod
    def get_stats():
        for _ in {
            1:"health",
            2:"damage",
            3:"luck"
        } :
            pass
"""



class Items(Model):
    id = PrimaryKeyField(null=False)
    name      = CharField()
    class Meta:
        database = connection.db
        table_name = "items"


class UserItems(Model):
    id = PrimaryKeyField(null=False)
    item_id = IntegerField()
    user_id = IntegerField()
    count   = IntegerField()

    @classmethod
    def get_user_items(cls,user_id):
        _items = UserItems\
            .select(UserItems)\
            .join(Items, on=(UserItems.item_id == Items.id)).alias('I')\
            .where(UserItems.user_id == user_id)
        return _items
    class Meta:
        database = connection.db
        table_name = "user_items"
