import sqlite3

# Function to drop a user by user_id
def drop_user(user_id):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    
    # Delete the user
    cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    
    # Optionally, delete related data (accounts, transactions) to maintain data consistency
    cursor.execute("DELETE FROM Accounts WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM Transactions WHERE account_id IN (SELECT account_id FROM Accounts WHERE user_id = ?)", (user_id,))
    
    conn.commit()
    conn.close()

# Function to drop an account by account_id
def drop_account(account_id):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    
    # Delete the account
    cursor.execute("DELETE FROM Accounts WHERE account_id = ?", (account_id,))
    
    # Delete related transactions for this account
    cursor.execute("DELETE FROM Transactions WHERE account_id = ?", (account_id,))
    
    conn.commit()
    conn.close()

# Function to drop a category by category_id
def drop_category(category_id):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    
    # Delete the category
    cursor.execute("DELETE FROM Categories WHERE category_id = ?", (category_id,))
    
    # Optionally, delete related transactions for this category
    cursor.execute("DELETE FROM Transactions WHERE category_id = ?", (category_id,))
    
    conn.commit()
    conn.close()

# Function to drop a transaction by transaction_id
def drop_transaction(transaction_id):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    
    # Delete the transaction
    cursor.execute("DELETE FROM Transactions WHERE transaction_id = ?", (transaction_id,))
    
    conn.commit()
    conn.close()

# Example usage
# drop_user(1)
# drop_account(2)
# drop_category(3)
# drop_transaction(4)
