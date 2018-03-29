from peewee import *

db = SqliteDatabase('data.db')
proxy_db = Proxy()


def init():
    Person.create_table()


class Person(Model):
    id = BigIntegerField()

    class Meta:
        database = db


class Action(Model):
    id = BigIntegerField()
    person_id = BigIntegerField()
    film = TextField()
    rating = BooleanField()

    class Meta:
        database = db
