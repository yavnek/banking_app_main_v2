import sqlite3
import random
from sqlite3 import Error

#Tworzenie połączenia bazy danych(jeżeli plik nie istnieje to zostaje stworzony) oraz tableli 
def create_connection_client(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        #Jeżeli bazy danych wcześniej nie było stwórz tabele
        cur.execute("CREATE TABLE bank_clients_table(account_number, name, surname, PESEL, balance, password)")
        cur.execute("CREATE TABLE bank_workers(worker_ID, name, surname, password)")
    except Error as e:
        print(e)
    
    return conn

#Tworzenie rzędu klienta
def create_bank_client(conn, bank_clients_entry):
    sql = ''' INSERT INTO bank_clients_table(account_number, name, surname, PESEL, balance, password)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, bank_clients_entry)
    conn.commit()
    return cur.lastrowid

def create_bank_worker(conn, bank_workers_entry):
    sql = ''' INSERT INTO bank_clients_table(worker_ID, name, surname, password)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, bank_workers_entry)
    conn.commit()
    return cur.lastrowid

#Funkcja sprawdzająca czy podana wartość istnieje w tabeli/kolumnie. Przydatne do sprawdzania czy nr konta istnieje 
def check_if_value_exists_in_db(table_name,column_name,comparable):
    conn = sqlite3.connect(r"database.db")
    cur = conn.cursor()
    cur.execute(f"SELECT {column_name} FROM {table_name}")
    try:
        column_index = None
        for idx, desc in enumerate(cur.description):
            if desc[0] == column_name:
                column_index = idx
                break

        for row in cur.fetchall():
            column_value = row[column_index]
            if column_value == comparable:
                return True
        

        conn.close()
        return False
    except Error as e:
        print(e)


    conn.close()
    return False

#Funkcja wyciągająca stan konta
def extract_account_balance(account_number):
    if(check_if_value_exists_in_db("bank_clients_table", "account_number", account_number)):
        conn = sqlite3.connect(r"database.db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM bank_clients_table WHERE account_number = ?", (account_number,))
        try:
            row = cur.fetchone()
            if row is not None:
                balance = row[0]
                conn.close()
                return balance
        except Error as e:
            print(e)
            return -1
    else:
        return -1

def subtract_money(account_number, money_value):
    if(check_if_value_exists_in_db("bank_clients_table", "account_number", account_number)and money_value>=0):
        conn = sqlite3.connect(r"database.db")
        cur = conn.cursor()

        cur.execute("SELECT balance FROM bank_clients_table WHERE account_number = ?", (account_number,))
        row = cur.fetchone()
        if row is not None:
            account_money = row[0]
        else:
            conn.close()
            return -1

        if(account_money>=money_value):
            account_money-=money_value
            cur.execute("UPDATE bank_clients_table SET balance = ? WHERE account_number = ?", (account_money, account_number))

            conn.commit()
            conn.close()
            return 1
        else:
            conn.close()
            return -1
    else:
        return -1
    
def add_money(account_number, money_value):
    if(check_if_value_exists_in_db("bank_clients_table", "account_number", account_number)and money_value>=0):
        conn = sqlite3.connect(r"database.db")
        cur = conn.cursor()

        cur.execute("SELECT balance FROM bank_clients_table WHERE account_number = ?", (account_number,))
        row = cur.fetchone()
        if row is not None:
            account_money = row[0]
            account_money+=money_value
            cur.execute("UPDATE bank_clients_table SET balance = ? WHERE account_number = ?", (account_money, account_number))

            conn.commit()
            conn.close()
            return 1
        else:
            conn.close()
            return -1
    else:
        return -1

# Przelew z jednego konta na drugie. Można jeszcze przerobić żeby zwracała odpowiednie wyjątki 
def transfer_money(sender_account_number, receiver_account_number, transferred_money):
    if (check_if_value_exists_in_db("bank_clients_table", "account_number", sender_account_number) and check_if_value_exists_in_db("bank_clients_table", "account_number", receiver_account_number) and transferred_money>=0):  
        conn = sqlite3.connect(r"database.db")
        cur = conn.cursor()


        # Retrieve sender's account balance
        cur.execute("SELECT balance FROM bank_clients_table WHERE account_number = ?", (sender_account_number,))
        row = cur.fetchone()
        if row is not None:
            sender_account_money = row[0]
        else:
            conn.close()
            return -1
        

        # Retrieve receiver's account balance
        cur.execute("SELECT balance FROM bank_clients_table WHERE account_number = ?", (receiver_account_number,))
        row = cur.fetchone()
        if row is not None:
            receiver_account_money = row[0]
        else:
            conn.close()
            return -1


        # Perform the money transfer
        if sender_account_money >= transferred_money:
            sender_account_money -= transferred_money
            receiver_account_money += transferred_money
            # Update sender's account balance
            cur.execute("UPDATE bank_clients_table SET balance = ? WHERE account_number = ?", (sender_account_money, sender_account_number))

            # Update receiver's account balance
            cur.execute("UPDATE bank_clients_table SET balance = ? WHERE account_number = ?", (receiver_account_money, receiver_account_number))

            conn.commit()
            conn.close()
            return 1
        else:
            conn.close()
            return -1
    else:
        return -1
    
def update_value_clients_table(column_name, account_number, updated_value):
    if check_if_value_exists_in_db("bank_clients_table", "account_number", account_number):
        conn = sqlite3.connect(r"database.db")
        cur = conn.cursor()
        try:
            query = f"UPDATE bank_clients_table SET {column_name} = ? WHERE account_number = ?"
            cur.execute(query, (updated_value, account_number))
            conn.commit()
            conn.close()
            return 1
        except Error as e:
            print(e)
            conn.close()
            return -1
    else:
        return -1
    
def update_value_workers_table(column_name, worker_ID, updated_value):
    if check_if_value_exists_in_db("bank_workers", "worker_ID", worker_ID):
        conn = sqlite3.connect(r"database.db")
        cur = conn.cursor()
        try:
            query = f"UPDATE bank_workers SET {column_name} = ? WHERE worker_ID = ?"
            cur.execute(query, (updated_value, worker_ID))
            conn.commit()
            conn.close()
            return 1
        except Error as e:
            print(e)
            conn.close()
            return -1
    else:
        return -1
    
def generate_random_account_number():
    try:
        rnd = random.randint(100000000000, 999999999999)
        while(check_if_value_exists_in_db("bank_clients_table", "account_number", rnd)):
            rnd = random.randint(100000000000, 999999999999)
        return rnd
    except Error as e:
        print(e)
        return -1

def main():
    conn = create_connection_client(r"database.db")
    with conn:
        #przy każdym nowym wpisie klienta trzeba sprawdzić czy już jego nr konta istnieje, ogólnie jak najczęściej używac tej funkcji "check_if_value_exists_in_db"
        account_number = generate_random_account_number()
        if  check_if_value_exists_in_db("bank_clients_table", "account_number", account_number)==False:
            bank_clients_entry = (account_number, 'jonatan', 'marek', 9000000000, 1000, '123456789') #zrobić funkcje z soceta która wpisuje dane do zmiennej entry 
            create_bank_client(conn, bank_clients_entry)#to też do powyższej funkcji można wrzucić jako już przypisanie
        account_number = 100000000001
        if check_if_value_exists_in_db("bank_clients_table", "account_number", account_number)==False:
            bank_clients_entry = (account_number, 'johan', 'maksym', 9000000000, 1000, '123456789')
            create_bank_client(conn, bank_clients_entry)
        transfer_money(100000000000, 100000000001, 500)

    update_value_clients_table("name", 100000000000, "Cris")
    print(extract_account_balance(100000000001))
    
    conn.close
    