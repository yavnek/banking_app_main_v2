import socket
import threading

HOST = "127.0.0.1"
PORT = 6666

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():

    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")
        quit()

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

def send_message(message):
    if message != '':
        client.sendall(message.encode())
    else:
        print("Message cannot be empty")

def listen_for_messages_from_server(client):

    while True:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            ...
        else:
            print("Message recevied from client is empty")

# main function
def main():

    connect()
    
if __name__ == '__main__':
    main()