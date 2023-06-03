import socket
import threading

HOST = "127.0.0.1"
PORT = 6666

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logged_in = True
user = ""

def connect():

    try:
        client.connect((HOST, PORT))
        print("Polaczono z serwerem")
    except:
        print(f"Nie udalo polaczyc sie z serwerem {HOST} {PORT}")
        quit()

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    while True:
        if(logged_in == True):
            logged_in_menu()
        else:
            start_menu()

def send_message(message):

    if message != '':
        client.sendall(message.encode())
    else:
        print("Wiadomosc nie moze byc pusta")

def listen_for_messages_from_server(client):

    while True:
        message = client.recv(2048).decode('utf-8')

        if message != '':
            print(message)
        else:
            print("Wiadomosc otrzymana od servera byla pusta")

def start_menu():
    print("1. Otworz konto")
    print("2. Zaloguj sie")

    print("\n9. Wyjscie")

    choice = input()

    match choice:
        case "1":
            open_an_account()
        case "2":
            login()
        case "9":
            client.close()
            quit()
        case _:
            print("Bledny wybor. Sprobuj ponownie.")

def open_an_account():
    name = input("Imie: ")
    surname = input("Nazwisko: ")
    pesel = input("PESEL: ")
    password = input("Haslo: ")

    try:
        send_message(f"open_an_account,{name}:{surname}:{pesel}:{password}")
    except:
        print("Wystapil blad, sprobuj ponownie")

def login():
    pesel = input("Numer konta: ")
    password = input("Haslo: ")

    send_message(f"login,{pesel}:{password}")

def logged_in_menu():
    print("1. Zobacz balans")
    print("2. Wplac pieniadze")
    print("3. Wyplac pieniadze")
    print("4. Wyslij pieniadze")
    print("5. Wyswietl dane konta")
    print("6. Wyloguj")
    print("\n9. Wyjdz")

    choice = input("Co chcesz zrobic?: ")

    match choice:
        case "1":
            check_balance()
        case "2":
            deposit_money()
        case "3":
            withdraw_money()
        case "4":
            send_money()
        case "5":
            show_account_details()
        case "6":
            logout()
        case "9":
            client.close()
            quit()
        case _:
            print("Bledny wybor. Sprobuj ponownie.")

def check_balance():
    send_message(f"check_balance,{user}")

def deposit_money():
    amount = input("Podaj ilość do wpłaty: ")

    send_message(f"deposit_money,{amount}")

def withdraw_money():
    amount = input("Podaj ilosc do wyplaty: ")

    send_message(f"withdraw_money,{amount}")

def send_money():
    amount = input("Podaj ilosc do wyslania: ")
    address = input("Podaj adres odbiorcy: ")

    send_message(f"send_money,{amount}:{address}")

def logout():
    send_message("logout")
    logged_in = False
    user = ""

def show_account_details():
    send_message(f"show_account_details,{user}")

def main():
    connect()
    
if __name__ == '__main__':
    main()