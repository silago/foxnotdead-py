from peewee import *
from . import connection
from . import stats

class Class(Model):
    id = PrimaryKeyField(null=False)
    name = CharField()

    class Meta:
        database = connection.db
        table_name = "classes"

class Levels(Model):
    id = PrimaryKeyField(null=False)
    exp = IntegerField()

    class Meta:
        database = connection.db
        table_name = "levels"

class ClassLevelStats(Model):
    id = PrimaryKeyField(null=False)
    class_id = IntegerField()
    level_id = IntegerField()
    container_id = IntegerField()

    class Meta:
        database = connection.db
        table_name = "class_level_stats"





