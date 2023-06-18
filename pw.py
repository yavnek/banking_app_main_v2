from ClientModel import db, Client


def connect():
    db.connect()

    db.create_tables([Client])


def create_client(accountNumber, firstName, lastName, PESEL, password):
    try:
        client = Client.create(accountNumber=accountNumber,
                               firstName=firstName,
                               lastName=lastName,
                               PESEL=PESEL,
                               password=password,
                               balance=0)
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


def account_details(accountNumber):
    client = Client.select().where(Client.accountNumber == accountNumber).get()
    return client

def check_if_value_exists(column, value):
    try:
        data = {column:value}
        client = Client.get(**data)
        return bool(client)
    except:
        return False
