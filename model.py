from peewee import *

from config import *

kekdb = SqliteDatabase('data.db')
db = PostgresqlDatabase('d45im87mi48anp',
                        user='lkejqvtkdsplqj',
                        password='ab3a4c08c45117ec8f1ca95c273e09e2af9babe51739001e52e474ec4701ac8b',
                        host='ec2-54-247-81-88.eu-west-1.compute.amazonaws.com',
                        port=5432)


def init_db():
    Chat.create_table()
    Action.create_table()

    Film.create_table()
    for i in MOVIES:
        Film.create(name=i)


class Chat(Model):
    id = BigIntegerField(primary_key=True)
    rating_stage = BooleanField(default=False)
    step = IntegerField(default=0)
    rate_one_film = IntegerField(default=0)

    class Meta:
        database = db


class Action(Model):
    chat_id = BigIntegerField()
    film = TextField()
    rating = BooleanField(null=True)

    class Meta:
        database = db


class Film(Model):
    name = TextField()

    class Meta:
        database = db
