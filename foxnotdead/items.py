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



"""
class UserInventory(Model):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField()
    item_id = IntegerField()
    slot_id = IntegerField()

    class Meta:
        database = connection.db
        table_name = "user_inventory"
"""


class Slots(Model):
    name = CharField()
    pass

class Items(Model):
    id = PrimaryKeyField(null=False)
    name = CharField()
    equipable = BooleanField()
    slot_id   = IntegerField()

    def get_user_item(self, user):
        result  = UserItems.get(UserItems.item_id == self.id, UserItems.user_id == user.id)
        return result

    class Meta:
        database = connection.db
        table_name = "items"


class UserItems(Model):
    from . import users
    id = PrimaryKeyField(null=False)
    item_id = IntegerField()
    # user_id = ForeignKeyField(users.User)
    user_id = foreign_field.ForeignKeyField(users.User, related_name="users")
    count = IntegerField()
    slot_id = IntegerField()

    def use(self, user, item):
        from . import stats
        #ui = _items.UserItems.get(_items.UserItems.item_id == item_id, _items.UserItems.user_id == user.id)
        if item.equipable:
            self.slot_id = item.slot_id
            self.save()
        else:
            self.count -= 1
            item_stats = ItemsStats.select().where(ItemsStats.item_id == self.item_id)
            user_stats = stats.UserStats.select().where(stats.UserStats.user_id == user.id)
            for item_stat in item_stats:
                for user_stat in user_stats:
                    if (user_stat.stat_id == item_stat.stat_id):
                        user_stat.value += item_stat.value
                        user_stat.save()
                        #result += "stat " + str(user_stat.stat_id) + "+= " + str(user_stat.value)
            #result += "\r\n"
            #result += str(ui.count) + " " + item.name + " left"


    def __unicode__(self):
        return str(self.item_id)

    @classmethod
    def get_user_items(cls, user_id, only_usable = False):
        if only_usable:
            _items = UserItems \
                .select(Items.id, Items.name, UserItems.count, Items.equipable, UserItems.slot_id) \
                .join(Items, on=(UserItems.item_id == Items.id)).alias('I') \
                .where(UserItems.user_id == user_id, UserItems.slot_id == 0)
        else:
            _items = UserItems \
                .select(Items.id, Items.name, UserItems.count, Items.equipable, UserItems.slot_id) \
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
