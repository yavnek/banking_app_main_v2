import socket
import threading
import db

HOST = '127.0.0.1'
PORT = 6666
active_clients = []
LISTENER_LIMIT = 5

def listen_for_messages(client, username):

    while True:

        message = client.recv(2048).decode('utf-8')
        # if message != '':
            
        #     final_msg = username + '~' + message
        #     send_messages_to_all(final_msg)

        # else:
        #     print(f"The message send from client {username} is empty")
        if (message == "check_balance"):
            send_message_to_client(db.extract_account_balance(account_number=...))


def send_message_to_client(client, message):

    client.sendall(message.encode())


def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

def client_handler(client):
    
    while True:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
        quit()

    db.main()

    server.listen()

    while True:
        client, address = server.accept()
        print(f"Client connected {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()