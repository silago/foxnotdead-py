from peewee import *
from . import connection
from . import foreign_field

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
    name = CharField()

    class Meta:
        database = connection.db
        table_name = "items"


class UserItems(Model):
    from . import users
    id = PrimaryKeyField(null=False)
    item_id = IntegerField()
    # user_id = ForeignKeyField(users.User)
    user_id = foreign_field._ForeignKeyField(users.User, related_name="users")
    count = IntegerField()

    def __unicode__(self):
        return str(self.item_id)

    @classmethod
    def get_user_items(cls, user_id):
        _items = UserItems \
            .select(Items.id, Items.name, UserItems.count) \
            .join(Items, on=(UserItems.item_id == Items.id)).alias('I') \
            .where(UserItems.user_id == user_id)

        return _items

    class Meta:
        database = connection.db
        table_name = "user_items"


class ItemsStats(Model):
    id = PrimaryKeyField(null=False)
    item_id = IntegerField()
    stat_id = IntegerField()
    value = IntegerField()

    class Meta:
        database = connection.db
        table_name = "item_stats"
