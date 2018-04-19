from peewee import *
import os

DATABASE = SqliteDatabase(
    'application/storage/main.db'
)
db = DATABASE
