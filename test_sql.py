# This file to to test SQL functions
import sqlite3

def test():
    conn = sqlite3.connect('finance_tracker.db')  # Connect to your database
    cursor = conn.cursor()

    cursor.execute("""
            SELECT 
                account_id, 
                transaction_date, 
                balance
            FROM 
                BalanceHistory
            WHERE 
                (account_id, transaction_date, history_id) IN (
                    SELECT 
                        account_id, 
                        transaction_date, 
                        MAX(history_id)
                    FROM 
                        BalanceHistory
                    GROUP BY 
                        account_id, 
                        transaction_date
                )
            ORDER BY 
                transaction_date;
            """)

    categories = cursor.fetchall()
    for category in categories:
        print(category)
    
    conn.close()


test()
