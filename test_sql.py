# This file to to test SQL functions
import sqlite3

def test_command():
    conn = sqlite3.connect('finance_tracker.db')  # Connect to your database
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM Categories
            """)

    categories = cursor.fetchall()
    for category in categories:
        print(category)
    
    conn.close()

test_command()
