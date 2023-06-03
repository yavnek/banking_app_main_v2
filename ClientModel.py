from peewee import *

db = SqliteDatabase('clients.db')

class Client(Model):
    accountNumber = IntegerField(primary_key=True)
    firstName = CharField()
    lastName = CharField()
    PESEL = CharField()
    password = CharField()
    balance = IntegerField()

    class Meta:
        database = db


