import socket
import json

HOST = '127.0.0.1'
PORT = 6666
ADDRESS = (HOST, PORT)
SIZE = 1024
FORMAT = "utf-8"
LOGGED_IN = False
LOGGED_CLIENT_NUMBER = ""
CONNECTED = False

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def main():
    print(f"Polaczono z serverem {HOST}:{PORT}")

    global CONNECTED
    CONNECTED = True

    while CONNECTED:
        if LOGGED_IN:
            logged_in_menu()
        else:
            start_menu()


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
            check_balance(LOGGED_CLIENT_NUMBER)
        case "2":
            deposit_money(LOGGED_CLIENT_NUMBER)
        case "3":
            withdraw_money(LOGGED_CLIENT_NUMBER)
        case "4":
            send_money(LOGGED_CLIENT_NUMBER)
        case "5":
            show_account_details(LOGGED_CLIENT_NUMBER)
        case "6":
            logout(LOGGED_CLIENT_NUMBER)
        case "9":
            global CONNECTED
            CONNECTED = False
            exit()
        case _:
            print("Nieprawidlowy wybor. Sprobuj ponownie\n")
    listen_for_messages_from_server(client)


def start_menu():
    print("1. Otworz konto")
    print("2. Zaloguj sie")

    print("\n9. Wyjscie")

    selection = input("> ")

    match selection:
        case "1":
            create_client()
        case "2":
            login()
        case "9":
            global CONNECTED
            CONNECTED = False
            exit()
        case _:
            print("Nieprawidlowy wybor. Sprobuj ponownie")
    listen_for_messages_from_server(client)


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
    global accountNumber
    accountNumber = input("Podaj numer konta: ").strip()
    password = input("Podaj haslo: ").strip()

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
    amount = int(input("Podaj ilośc: ").strip())

    msg = {
        "command": "DEPOSIT_MONEY",
        "accountNumber": accountNumber,
        "amount": amount
    }

    client.send(json.dumps(msg).encode(FORMAT))


def withdraw_money(accountNumber):
    amount = int(input("Podaj ilośc: ").strip())

    msg = {
        "command": "WITHDRAW_MONEY",
        "accountNumber": accountNumber,
        "amount": amount
    }

    client.send(json.dumps(msg).encode(FORMAT))


def send_money(senderAccountNumber):
    receiverAccountNumber = input("Podaj adres odbiorcy: ").strip()
    amount = int(input("Podaj ilosc: ").strip())

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


def logout(accountNumber):
    msg = {
        "command": "LOGOUT",
        "accountNumber": accountNumber
    }

    client.send(json.dumps(msg).encode(FORMAT))

    global LOGGED_IN
    global LOGGED_CLIENT_NUMBER

    LOGGED_IN = False
    LOGGED_CLIENT_NUMBER = ""


def exit():
    msg = {
        "command": "EXIT"
    }

    client.send(json.dumps(msg).encode(FORMAT))


def logged_in():
    global LOGGED_IN
    global LOGGED_CLIENT_NUMBER

    LOGGED_IN = True
    LOGGED_CLIENT_NUMBER = accountNumber
    print(f"Zalogowano jako {LOGGED_CLIENT_NUMBER}")


def listen_for_messages_from_server(client):
    message = client.recv(SIZE).decode(FORMAT)
    if (message == 'CLIENT_LOGIN'):
        logged_in()
    else:
        print(message)


if __name__ == "__main__":
    main()
