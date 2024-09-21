import sqlite3

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
def insert_transaction(account_id, category_id, amount, transaction_type, description, transaction_date):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Insert transaction (amount is already positive for income and negative for expense)
            cursor.execute("""INSERT INTO Transactions (account_id, category_id, amount, 
                                                        transaction_type, description, transaction_date)
                              VALUES (?, ?, ?, ?, ?, ?)""", 
                           (account_id, category_id, amount, transaction_type, description, transaction_date))
            
            # Update balance (no need to check transaction type)
            cursor.execute("UPDATE Accounts SET balance = balance + ? WHERE account_id = ?", 
                           (amount, account_id))
            
            conn.commit()
            print("Transaction inserted and account balance updated successfully!")
        except sqlite3.Error as e:
            print(f"Error inserting transaction: {e}")
        finally:
            conn.close()

