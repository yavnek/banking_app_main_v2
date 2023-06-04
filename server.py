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
                pw.create_client(msg['firstName'], msg['lastName'], msg['PESEL'], msg['password'])
            case "GET_ACCOUNT_BALANCE":
                balance = pw.get_account_balance(msg['accountNumber'])

            case "DEPOSIT_MONEY":
                pw.deposit_money(msg['accountNumber'], msg['amount'])
            case "WITHDRAW_MONEY":
                pw.withdraw_money(msg['accountNumber'], msg['amount'])
            case "TRANSFER_MONEY":
                pw.transfer_money(msg['senderAccountNumber'], msg['receiverAccountNumber'], msg['amount'])
            case DISCONNECT_MSG:
                connected = False

        print(f"[{addr}] {msg}")

        #conn.send(msg.encode(FORMAT))


    conn.close()

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
