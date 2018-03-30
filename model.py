from peewee import *

db = SqliteDatabase('data.db')
proxy_db = Proxy()


def init_db():
    Chat.create_table()
    Action.create_table()


class Chat(Model):
    id = BigIntegerField(primary_key=True)
    rating_stage = BooleanField(default=False)
    step = IntegerField(default=0)

    class Meta:
        database = db


class Action(Model):
    id = BigIntegerField()
    person_id = BigIntegerField()
    film = TextField()
    rating = BooleanField()

    class Meta:
        database = db
