import sqlite3

def total_balance():
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT account_name, SUM(balance) FROM Accounts GROUP BY account_name")
    results = cursor.fetchall()
    conn.close()
    return results

def total_expenses_for_month(month):
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT SUM(amount) FROM Transactions WHERE transaction_type = 'expense' AND strftime('%m', transaction_date) = '{month}'")
    result = cursor.fetchone()
    conn.close()
    return result[0]

def category_wise_breakdown():
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.category_name, SUM(t.amount)
        FROM Transactions t
        JOIN Categories c ON t.category_id = c.category_id
        WHERE t.transaction_type = 'expense'
        GROUP BY c.category_name
    """)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
print(total_balance())
print(total_expenses_for_month('09'))  # September
print(category_wise_breakdown())
