from peewee import *
import os

db_type = os.environ.get("db_type","")
db_name = os.environ.get("db_name","")
db_user = os.environ.get("db_user","")
db_pass = os.environ.get("db_pass","")
db_host = os.environ.get("db_host","")
db_port = os.environ.get("db_port","")

print(db_type)
if (db_type == "pg"):
    DATABASE = PostgresqlDatabase(db_name, user=db_user, password=db_pass,
                           host=db_host, port=db_port)
else:
    DATABASE = SqliteDatabase(
        db_name
        #'/home/silago/PycharmProjects/pyfoxnotdead/application/storage/main.db'
    )

db = DATABASE
