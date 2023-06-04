import socket
import json

HOST = '127.0.0.1'
PORT = 6666
ADDRESS = (HOST, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "9"
LOGGED_IN = True
connected = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def main():
    print(f"Polaczono z serverem {HOST}:{PORT}")


    while connected:

        if LOGGED_IN:
            logged_in_menu()
        else:
            start_menu()


def start_menu():
    print("1. Otworz konto")
    print("2. Zaloguj sie")

    print("\n9. Wyjscie")

    selection = input("> ")

    match selection:
        case "1":
            create_client()
        case "2":
            ...
        case "9":
            connected = False
        case _:
            print("Nieprawidlowy wybor. Sprobuj ponownie")


def logged_in_menu():
    print("1. Zobacz balans")
    print("2. Wplac pieniadze")
    print("3. Wyplac pieniadze")
    print("4. Wyslij pieniadze")
    print("5. Wyswietl dane konta")
    print("6. Wyloguj")
    print("\n9. Wyjdz")

    selection = input("> ")

    match selection:
        case "1":
            check_balance(21567)
        case "2":
            ...
        case "3":
            ...
        case "4":
            ...
        case "5":
            ...
        case "6":
            ...
        case "9":
            ...
        case _:
            print("Nieprawidlowy wybor. Sprobuj ponownie")

def create_client():
    firstName = input("Imie: ").strip()
    lastName = input("Nazwisko: ").strip()
    PESEL = input("PESEL: ").strip()
    password = input("Haslo: ").strip()

    msg = {
        "command": "CREATE_CLIENT",
        "firstName": firstName,
        "lastName": lastName,
        "PESEL": PESEL,
        "password": password
    }

    client.send(json.dumps(msg).encode(FORMAT))

def login():
    accountNumber = input("Podaj numer konta: ")
    password = input("Podaj haslo: ")

    msg = {
        "command": "LOGIN",
        "accountNumber": accountNumber,
        "password": password
    }

    client.send(json.dumps(msg).encode(FORMAT))
def check_balance(accountNumber):
    msg = {
        "command": "GET_ACCOUNT_BALANCE",
        "accountNumber": accountNumber
    }

    client.send(json.dumps(msg).encode(FORMAT))

def deposit_money(accountNumber):
    amount = int(input("Podaj ilośc: ")).strip()

    msg = {
        "command": "DEPOSIT_MONEY",
        "accountNumber": accountNumber,
        "amount": amount
    }

    client.send(json.dumps(msg).encode(FORMAT))


def withdraw_money(accountNumber):
    amount = int(input("Podaj ilośc: ")).strip()

    msg = {
        "command": "WITHDRAW_MONEY",
        "accountNumber": accountNumber,
        "amount": amount
    }

    client.send(json.dumps(msg).encode(FORMAT))

def send_money(senderAccountNumber):
    receiverAccountNumber = input("Podaj adres odbiorcy: ").strip()
    amount = int(input("Podaj ilosc: "))

    msg = {
        "command": "TRANSFER_MONEY",
        "receiverAccountNumber": receiverAccountNumber,
        "senderAccountNumber": senderAccountNumber,
        "amount": amount
    }

    client.send(json.dumps(msg).encode(FORMAT))

def show_account_details(accountNumber):
    msg = {
        "command": "SHOW_ACCOUNT_DETAILS",
        "accountNumber": accountNumber
    }

    client.send(json.dumps(msg).encode(FORMAT))

if __name__ == "__main__":
    main()
