import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


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

def fetch_expenses_by_month_year():
    conn = sqlite3.connect('finance_tracker.db')
    query = """
        SELECT  strftime('%Y', transaction_date) AS year, 
                strftime('%m', transaction_date) AS month, 
                SUM(amount) AS total_spent
        FROM Transactions
        WHERE transaction_type = 'expense'
        GROUP BY year, month
        ORDER BY year, month
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_expenses_by_month_year():
    df = fetch_expenses_by_month_year()

    # Combine year and month into one column for better readability in the plot
    df['year_month'] = df['year'] + '-' + df['month']

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['year_month'], df['total_spent'], marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45)
    plt.xlabel('Month-Year')
    plt.ylabel('Total Spent')
    plt.title('Total Spending by Month and Year')
    plt.grid(True)
    plt.tight_layout()

    plt.show()