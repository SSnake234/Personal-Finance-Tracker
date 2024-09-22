import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


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
    result = cursor.fetchall()
    conn.close()
    return result[0]

def category_wise_breakdown():
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.account_id, c.category_name, SUM(t.amount)
        FROM Transactions t
        JOIN Categories c ON t.category_id = c.category_id
        WHERE t.transaction_type = 'expense'
        GROUP BY c.category_name
    """)
    results = cursor.fetchall()
    conn.close()
    return results


#Visualizing expenses
def fetch_expenses_of_days_in_month(account_id, month, year):
    try:
        conn = sqlite3.connect('finance_tracker.db')
        query = """
            SELECT strftime('%d', transaction_date) AS day, 
                   ((0 - SUM(amount)) / 1000) AS total_spent
            FROM Transactions
            WHERE amount < 0
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

def plot_expenses_by_month(account_id, month, year):
    df = fetch_expenses_of_days_in_month(account_id, month, year)

    if df.empty:
        print(f"No expenses found for {month}-{year} with account ID {account_id}.")
        return

    # Get the first and last available day in the dataset
    first_available_day = df['day'].min()
    last_available_day = int(df['day'].max())
    # Generate the full range of days between the first and last available days
    full_range_days = pd.DataFrame([f"{day:02d}" for day in range(int(first_available_day), int(last_available_day) + 1)], columns=['day'])

    # Merge with the fetched expense data, fill missing total_spent with 0 within available range
    df_full = full_range_days.merge(df, on='day', how='left').fillna(0)

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



#Visualizing balance history at the end of day
def fetch_balance_history_of_days_in_month(account_id, month, year):
    try:
        conn = sqlite3.connect('finance_tracker.db')
        query = """
            SELECT strftime('%d', transaction_date) AS day, 
                   balance AS balance_at_end_of_day
            FROM BalanceHistory
            WHERE account_id = ?
            AND strftime('%m', transaction_date) = ?
            AND strftime('%Y', transaction_date) = ?
            AND (account_id, transaction_date, history_id) IN (
                SELECT account_id, transaction_date, MAX(history_id)
                FROM BalanceHistory
                WHERE account_id = ?
                AND strftime('%m', transaction_date) = ?
                AND strftime('%Y', transaction_date) = ?
                GROUP BY account_id, transaction_date
            )
            ORDER BY transaction_date
        """
        df = pd.read_sql_query(query, conn, params=(account_id, month, year, account_id, month, year))

        return df
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame() 
    finally:
        if conn:
            conn.close()

def plot_balance_history_by_month(account_id, month, year):
    df = fetch_balance_history_of_days_in_month(account_id, month, year)

    if df.empty:
        print(f"No balance history found for {month}-{year} with account ID {account_id}.")
        return

    # Get the first and last available day in the dataset
    first_available_day = df['day'].min()
    last_available_day = int(df['day'].max())

    # Generate the full range of days between the first and last available days
    full_range_days = pd.DataFrame([f"{day:02d}" for day in range(int(first_available_day), int(last_available_day) + 1)], columns=['day'])

    # Merge the data with the full range of days
    df_full = full_range_days.merge(df, on='day', how='left')

    # Forward fill missing balances only within the available date range
    df_full['balance_at_end_of_day'] = df_full['balance_at_end_of_day'].ffill()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(df_full['day'], df_full['balance_at_end_of_day'], marker='o', linestyle='-', color='g')
    plt.xticks(rotation=45)
    plt.xlabel('Day')
    plt.ylabel('Balance (VND)')
    plt.title(f'Balance History in {month}-{year}')
    plt.grid(True)
    plt.ylim(0) 
    plt.tight_layout()
    plt.show()