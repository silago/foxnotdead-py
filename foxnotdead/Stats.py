from . import commands
from peewee import *
import application.foxnotdead.connection as connection


class UserStats(Model):
    id = PrimaryKeyField(null=False)
    stat_id =
    user_id =

class Stats(Model):
    id = PrimaryKeyField(null=False)
    name = CharField(null=False)

    class Meta:
        database = connection.db
        table_name = "states"



