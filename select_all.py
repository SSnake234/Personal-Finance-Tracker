import sqlite3

def list_transactions():
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Transactions;")

    categories = cursor.fetchall()
    print("Transactions in the database:")
    for category in categories:
        print(category)
    
    conn.close()


list_transactions()
