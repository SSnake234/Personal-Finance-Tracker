import sqlite3

connection = sqlite3.connect("finance_tracker.db")
cursor = connection.cursor()

# Create Users table
create_users_table = """
CREATE TABLE IF NOT EXISTS Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
"""

# Create Accounts table
create_accounts_table = """
CREATE TABLE IF NOT EXISTS BalanceHistory (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    balance REAL,
    transaction_date DATE,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
)
"""

# Create Categories table
create_categories_table = """
CREATE TABLE IF NOT EXISTS Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
)
"""

# Create Transactions table
create_transactions_table = """
CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    category_id INTEGER,
    amount REAL,
    transaction_type TEXT,
    description TEXT,
    transaction_date DATE,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
)
"""

#Create Balance_history table
create_balancehis_table = """
CREATE TABLE IF NOT EXISTS BalanceHistory (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    balance REAL,
    transaction_date DATE,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);
"""

# Execute the table creation queries
cursor.execute(create_users_table)
cursor.execute(create_accounts_table)
cursor.execute(create_categories_table)
cursor.execute(create_transactions_table)
cursor.execute(create_balancehis_table)

connection.commit()
connection.close()
