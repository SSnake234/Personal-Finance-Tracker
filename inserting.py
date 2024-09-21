import sqlite3

def insert_user(username, email, password):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)", 
                   (username, email, password))
    conn.commit()
    conn.close()
    
def insert_account(user_id, account_name, bank, balance):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Accounts (user_id, account_name, bank, balance) VALUES (?, ?, ?, ?)", 
                   (user_id, account_name, bank, balance))
    conn.commit()
    conn.close()
    
def insert_category(category_name):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Categories (category_name) VALUES (?)", (category_name,))
    conn.commit()
    conn.close()

def insert_transaction(account_id, category_id, amount, transaction_type, description, transaction_date):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Transactions (account_id, category_id, amount, 
                                                transaction_type, description, transaction_date)
                      VALUES (?, ?, ?, ?, ?, ?)""", 
                   (account_id, category_id, amount, 
                    transaction_type, description, transaction_date))
    cursor.execute("""
                   UPDATE Accounts SET balance = balance + ? WHERE account_id = ?
                   """, (amount, account_id))
    conn.commit()
    conn.close()

