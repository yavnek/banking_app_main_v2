import socket
import threading
import pw
import json
import random

HOST = '127.0.0.1'
PORT = 6666
ADDRESS = (HOST, PORT)
SIZE = 1024
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(conn, addr):
    print(f"\n[NOWE POLACZENIE] {addr}")

    CONNECTED = True
    while CONNECTED:
        msg = conn.recv(SIZE).decode(FORMAT)
        msg = json.loads(msg)
        match msg['command']:
            case "CREATE_CLIENT":
                create_client_command(msg['firstName'], msg['lastName'], msg['PESEL'], msg['password'])
            case "LOGIN":
                login_command(msg['accountNumber'], msg['password'])
            case "GET_ACCOUNT_BALANCE":
                get_account_balance_command(msg['accountNumber'])
            case "DEPOSIT_MONEY":
                deposit_money_command(msg['accountNumber'], msg['amount'])
            case "WITHDRAW_MONEY":
                withdraw_money_command(msg['accountNumber'], msg['amount'])
            case "TRANSFER_MONEY":
                transfer_money_command(msg['senderAccountNumber'], msg['receiverAccountNumber'], msg['amount'])
            case "SHOW_ACCOUNT_DETAILS":
                show_account_details_command(msg['accountNumber'])
            case "LOGOUT":
                logout_command(msg['accountNumber'])
            case "EXIT":
                CONNECTED = False
                conn.close()

        print(f"[{addr}] {msg}")

    conn.close()


def create_client_command(firstName, lastName, PESEL, password):
    while True:
        accountNumber = random.randint(1, 50000)
        accountNumberExists = pw.check_if_value_exists("accountNumber", accountNumber)
        if (accountNumberExists == False):
            break

    pw.create_client(accountNumber, firstName, lastName, PESEL, password)

    send_msg_to_client(f"Stworzono nowe konto. Twoj numer konta to {accountNumber}")


def login_command(accountNumber, password):
    try:
        client = pw.account_details(accountNumber)
        if (client.password == password):
            send_msg_to_client("CLIENT_LOGIN")
        else:
            send_msg_to_client("Zle haslo. Sprobuj ponownie")
    except:
        send_msg_to_client("Brak takiego konta. Spróbuj ponownie")


def get_account_balance_command(accountNumber):
    balance = pw.get_account_balance(accountNumber)
    msg = f"\nBalans konta {accountNumber} to: {balance}"
    send_msg_to_client(msg)


def deposit_money_command(accountNumber, amount):
    if (amount < 0):
        msg = "Wplata nie moze byc mniejsza od zera"
    else:
        pw.deposit_money(accountNumber, amount)
        msg = f"Wplacono: {amount}"

    send_msg_to_client(msg)


def withdraw_money_command(accountNumber, amount):
    balance = pw.get_account_balance(accountNumber)

    if (amount > balance):
        msg = "Masz za malo pieniedzy"
    elif (amount < 0):
        msg = "Nie mozna wyplacic kwoty mniejszej od zera"
    else:
        pw.withdraw_money(accountNumber, amount)
        msg = f"Wyplacono: {amount}"

    send_msg_to_client(msg)


def transfer_money_command(senderAccountNumber, receiverAccountNumber, amount):
    senderBalance = pw.get_account_balance(senderAccountNumber)

    if (amount > senderBalance):
        msg = "Masz za malo pieniedzy"
    else:
        pw.transfer_money(senderAccountNumber, receiverAccountNumber, amount)
        msg = f"Wyslano {amount} do {receiverAccountNumber}"

    send_msg_to_client(msg)


def show_account_details_command(accountNumber):
    client = pw.account_details(accountNumber)

    msg = f"Numer konta: {client.accountNumber}\n" \
          f"Imie: {client.firstName}\n" \
          f"Nazwisko: {client.lastName}\n" \
          f"PESEL: {client.PESEL}\n" \
          f"Haslo: {client.password}\n" \
          f"Balans: {client.balance}"

    send_msg_to_client(msg)


def logout_command(accountNumber):
    send_msg_to_client(f"Klient {accountNumber} wylogowany")


def send_msg_to_client(message):
    conn.send(str(message).encode(FORMAT))


def main():
    pw.connect()
    server.listen()
    print(f"[NASLUCHIWANIE] Server nasluchuje na {HOST}:{PORT}")
    while True:
        global conn
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[AKTYWNE POLACZENIA] {threading.active_count() - 1}")


if __name__ == "__main__":
    main()
