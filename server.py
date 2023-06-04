import socket
import threading
from ClientModel import db
import pw
import json

HOST = '127.0.0.1'
PORT = 6666
ADDRESS = (HOST, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "9"

def handle_client(conn, addr):
    print(f"[NOWE POLACZENIE] {addr}")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        msg = json.loads(msg)
        match msg['command']:
            case "CREATE_CLIENT":
                create_client_command(msg['firstName'], msg['lastName'], msg['PESEL'], msg['password'])
            case "GET_ACCOUNT_BALANCE":
                get_account_balance_command(msg['accountNumber'])
            case "DEPOSIT_MONEY":
                deposit_money_command(msg['accountNumber'], msg['amount'])
            case "WITHDRAW_MONEY":
                withdraw_money_command(msg['accountNumber'], msg['amount'])
            case "TRANSFER_MONEY":
                transfer_money_command(msg['senderAccountNumber'], msg['receiverAccountNumber'], msg['amount'])
            case DISCONNECT_MSG:
                connected = False

        print(f"[{addr}] {msg}")

        #conn.send(msg.encode(FORMAT))


    conn.close()

def create_client_command(firstName, lastName, PESEL, password):
    pw.create_client(firstName, lastName, PESEL, password)

def get_account_balance_command(accountNumber):
    pw.get_account_balance(accountNumber)

def deposit_money_command(accountNumber, amount):
    pw.deposit_money(accountNumber, amount)

def withdraw_money_command(accountNumber, amount):
    pw.withdraw_money(accountNumber, amount)

def transfer_money_command(senderAccountNumber, receiverAccountNumber, amount):
    pw.transfer_money(senderAccountNumber, receiverAccountNumber, amount)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen()
    print(f"[NASLUCHIWANIE] Server nasluchuje na {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[AKTYWNE POLACZENIA] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
