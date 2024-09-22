import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from calendar import monthrange


#Analysing
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


#Visualizing expenses
# Fetch expenses per day in the given month
def fetch_expenses_of_days_in_month(account_id, month, year):
    try:
        conn = sqlite3.connect('finance_tracker.db')
        query = """
            SELECT strftime('%d', transaction_date) AS day, 
                   ((0 - SUM(amount)) / 1000) AS total_spent
            FROM Transactions
            WHERE transaction_type = 'expense'
            AND account_id = ?
            AND strftime('%m', transaction_date) = ?
            AND strftime('%Y', transaction_date) = ?
            GROUP BY day
            ORDER BY day
        """
        df = pd.read_sql_query(query, conn, params=(account_id, month, year)) 
        return df
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame() 
    finally:
        if conn:
            conn.close()

# Generate all days of the month as a DataFrame
def generate_full_month_days(month, year):
    num_days = monthrange(int(year), int(month))[1]
    days = [f"{day:02d}" for day in range(1, num_days + 1)]
    full_month_df = pd.DataFrame(days, columns=['day'])
    return full_month_df

# Plot expenses for a given month
def plot_expenses_by_month(account_id, month, year):
    df = fetch_expenses_of_days_in_month(account_id, month, year)

    if df.empty:
        print(f"No expenses found for {month}-{year} with account ID {account_id}.")
        return

    # Merge with existing data, fill missing total_spent with 0
    full_month_df = generate_full_month_days(month, year)
    df_full = full_month_df.merge(df, on='day', how='left').fillna(0)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df_full['day'], df_full['total_spent'], marker='o', linestyle='-', color='b')
    plt.xticks(rotation=45)
    plt.xlabel('Day')
    plt.ylabel('Total Spent (in 1k VND)')
    plt.title(f'Total Spending in {month}-{year}')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#plot_expenses_by_month(1, '09', '2024')