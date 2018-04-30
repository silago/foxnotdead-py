from peewee import *
import os

db_type = os.environ["db_type"]
db_name = os.environ["db_name"]
db_user = os.environ["db_user"]
db_pass = os.environ["db_pass"]
db_host = os.environ["db_host"]
db_port = os.environ["db_port"]


if (db_type == "pg"):
    PostgresqlDatabase(db_name, user=db_user, password=db_pass,
                           host=db_host, port=db_port)
else:
    DATABASE = SqliteDatabase(
        db_name
        #'/home/silago/PycharmProjects/pyfoxnotdead/application/storage/main.db'
    )

db = DATABASE
