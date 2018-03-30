from peewee import *

kekdb = SqliteDatabase('data.db')
db = PostgresqlDatabase('d55juqn67jac81',
                        user='ildwfawbdhxfbs',
                        password='2fa2d45e7c6f6b6b9dbd92d5a34d35225858573baacf0782599bbd5ad3c62f65',
                        host='ec2-54-75-227-92.eu-west-1.compute.amazonaws.com',
                        port=5432)


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
    chat_id = BigIntegerField()
    film = TextField()
    rating = BooleanField(null=True)

    class Meta:
        database = db
