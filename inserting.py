import sqlite3
import datetime

# Utility function to connect to the database
def get_db_connection():
    try:
        conn = sqlite3.connect('finance_tracker.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Insert user into the database
def insert_user(username, email, password):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)", 
                           (username, email, password))
            conn.commit()
            print("User inserted successfully!")
        except sqlite3.Error as e:
            print(f"Error inserting user: {e}")
        finally:
            conn.close()

# Insert account into the database
def insert_account(user_id, account_name, balance):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Accounts (user_id, account_name, balance) VALUES (?, ?, ?)", 
                           (user_id, account_name, balance))
            conn.commit()
            print("Account inserted successfully!")
        except sqlite3.Error as e:
            print(f"Error inserting account: {e}")
        finally:
            conn.close()

# Insert category into the database
def insert_category(category_name):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Categories (category_name) VALUES (?)", (category_name,))
            conn.commit()
            print("Category inserted successfully!")
        except sqlite3.Error as e:
            print(f"Error inserting category: {e}")
        finally:
            conn.close()

# Insert transaction and update account balance
def insert_transaction(account_id, category_id, amount, description, transaction_date):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Insert transaction
            cursor.execute("""INSERT INTO Transactions (account_id, category_id, amount, 
                                                        description, transaction_date)
                              VALUES (?, ?, ?, ?, ?)""", 
                           (account_id, category_id, amount, description, transaction_date))
            
            # Update balance in the account
            cursor.execute("UPDATE Accounts SET balance = balance + ? WHERE account_id = ?", 
                           (amount, account_id))
            
            # Update balance history of the account
            update_balance_history(account_id, transaction_date)
            
            conn.commit()
            print("Transaction inserted and account balance updated successfully!")
        except sqlite3.Error as e:
            print(f"Error inserting transaction: {e}")
        finally:
            conn.close()

# Function to update account balance history after a transaction
def update_balance_history(account_id, transaction_date):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Fetch the current balance from Accounts table (already updated)
            cursor.execute("SELECT balance FROM Accounts WHERE account_id = ?", (account_id,))
            current_balance = cursor.fetchone()[0]

            # Insert the updated balance into the BalanceHistory table
            cursor.execute("""INSERT INTO BalanceHistory (account_id, balance, transaction_date) 
                              VALUES (?, ?, ?)""",
                           (account_id, current_balance, transaction_date))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating balance history: {e}")
        finally:
            conn.close()