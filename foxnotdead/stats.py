from . import commands
from peewee import *
from . import connection






class StatsHolder(Model):
    id = PrimaryKeyField(null=False)
    container_id = IntegerField()
    stat_id =  IntegerField()
    value   =  IntegerField()

    class Meta:
        database = connection.db
        table_name = "stats_holder"


class UserStats(Model):
    from . import users

    id = PrimaryKeyField(null=False)
    stat_id = IntegerField()
    user_id = IntegerField()
    value   = IntegerField()

    class Meta:
        database = connection.db
        table_name = "user_stats"

class Stats(Model):
    id = PrimaryKeyField(null=False)
    name = CharField()
    key  = CharField()

    @classmethod
    def all(cls):
        return Stats.select(cls).where(True)

    class Meta:
        database = connection.db
        table_name = "stats"
