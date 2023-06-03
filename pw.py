from ClientModel import db, Client
import random
from peewee import *

db.connect()

db.create_tables([Client])

def create_client(firstName, lastName, PESEL, password):
    accountNumber = random.randint(1, 50000)

    try:
        client = Client.create(accountNumber=accountNumber,firstName=firstName,lastName=lastName,PESEL=PESEL,password=password,balance=0)
        client.save()
    except Exception as ex:
        print(ex)
def get_account_balance(accountNumber):
    client = Client.select().where(Client.accountNumber == accountNumber).get()

    return client.balance

def withdraw_money(accountNumber, amount):
    client = Client.select().where(Client.accountNumber == accountNumber).get()
    client.balance = client.balance - amount
    client.save()

def deposit_money(accountNumber, amount):
    client = Client.select().where(Client.accountNumber == accountNumber).get()
    client.balance = client.balance + amount
    client.save()

def transfer_money(senderAccountNumber, receiverAccountNumber, amount):
    withdraw_money(senderAccountNumber, amount)
    deposit_money(receiverAccountNumber, amount)

def check_if_value_exists(column, value):
    try:
        client = Client.get(column == value)
        return bool(client)
    except:
        return False

print(get_account_balance(2))



