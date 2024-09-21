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

#VISUALIZATION
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

    df['month-year'] = df['month'] + '-' + df['year']

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df['month-year'], df['total_spent'], marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45)
    plt.xlabel('Month-Year')
    plt.ylabel('Total Spent')
    plt.title('Total Spending by Month and Year')
    plt.grid(True)
    plt.tight_layout()

    plt.show()


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def fetch_transactions_for_month(account_id, year, month):
    """Fetch transactions for a specific account and month."""
    conn = sqlite3.connect('finance_tracker.db')
    query = """
    SELECT transaction_date, amount
    FROM Transactions
    WHERE account_id = ? AND strftime('%Y', transaction_date) = ? AND strftime('%m', transaction_date) = ?
    ORDER BY transaction_date
    """
    df = pd.read_sql_query(query, conn, params=(account_id, year, month))
    conn.close()
    return df

def calculate_cumulative_balance(df, starting_balance):
    """Calculate the cumulative balance over time."""
    df['cumulative_balance'] = df['amount'].cumsum() + starting_balance
    return df

def plot_balance_over_month(df):
    """Plot balance changes over time."""
    plt.figure(figsize=(10, 6))
    plt.plot(df['transaction_date'], df['cumulative_balance'], marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Cumulative Balance')
    plt.title('Account Balance Throughout the Month')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Example usage
def visualize_balance_for_month(account_id, starting_balance, year, month):
    transactions_df = fetch_transactions_for_month(account_id, year, month)
    if not transactions_df.empty:
        transactions_df = calculate_cumulative_balance(transactions_df, starting_balance)
        plot_balance_over_month(transactions_df)
    else:
        print("No transactions found for this month.")
