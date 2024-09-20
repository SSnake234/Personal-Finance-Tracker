import sqlite3

connection = sqlite3.connect("finance_tracker.db")
cursor = connection.cursor()

create_users_table = """
CREATE TABLE IF NOT EXISTS Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
)
"""

create_accounts_table = """
CREATE TABLE IF NOT EXISTS Accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    bank TEXT,
    balance REAL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)
"""

create_categories_table = """
CREATE TABLE IF NOT EXIST Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL,
)
"""

create_transactions_table = """
CREATE TABLE IF NOT EXIST Transactions (
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


cursor.execute(create_users_table)
cursor.execute(create_accounts_table)
cursor.execute(create_categories_table)
cursor.execute(create_transactions_table)

