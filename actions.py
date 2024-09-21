import sqlite3
import inserting  
import analysis_and_visualize

def inserting_action():
    """Handles insertion of users, accounts, categories, and transactions."""
    print(
    """Choose inserting:
        1 for inserting user
        2 for inserting account
        3 for inserting category
        4 for inserting transaction"""
        )
    
    try:
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            insert_user()
        elif choice == 2:
            insert_account()
        elif choice == 3:
            insert_category()
        elif choice == 4:
            insert_transaction()
        else:
            print("Invalid choice! Please choose between 1 and 4.")
    except ValueError:
        print("Invalid input! Please enter a number.")

def insert_user():
    """Inserts a new user into the system."""
    print("Inserting user...")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    inserting.insert_user(username, email, password)
    print("User inserted successfully!")

def insert_account():
    """Inserts a new account for a user."""
    print("Inserting account...")
    try:
        user_id = int(input("Enter user ID: "))
        account_name = input("Enter account name (Name - Bank): ")
        balance = float(input("Enter account balance: "))
        inserting.insert_account(user_id, account_name, balance)
        print("Account inserted successfully!")
    except ValueError:
        print("Invalid input! Please ensure that user ID and balance are numbers.")

def insert_category():
    """Inserts a new category."""
    print("Inserting category...")
    category_name = input("Enter category name: ")
    inserting.insert_category(category_name)
    print("Category inserted successfully!")

def insert_transaction():
    """Inserts a new transaction."""
    print("Inserting transaction...")
    try:
        account_id = int(input("Enter account ID: "))
        category_id = int(input(
            """Enter category ID (1: Food; 2: Rent; 3: Utilities; 4: Clothing; 5: Travel;
            6: Health; 7: Salary + Income; 8: Others): """
            ))
        amount = float(input("Enter amount: "))
        transaction_type = input("Enter transaction type (income/expense): ").lower()
        if transaction_type not in ['income', 'expense']:
            raise ValueError("Invalid transaction type!")
        description = input("Enter description: ")
        transaction_date = input("Enter transaction date (YYYY-MM-DD): ")
        inserting.insert_transaction(account_id, category_id, amount, transaction_type, description, transaction_date)
        print("Transaction inserted successfully!")
    except ValueError as ve:
        print(f"Error: {ve}")

def analysis_action():
    """Handles financial analysis like balance, expenses, and category breakdown."""
    print(
    """Choose analysis:
        1 for total balance
        2 for total expenses for a month
        3 for category-wise breakdown
        4 for visualize spending by month and year
        """)
    try:
        analysis_choice = int(input("Enter your choice: "))
        
        if analysis_choice == 1:
            print("Total Balance: ")
            print(analysis_and_visualize.total_balance())
        elif analysis_choice == 2:
            month = input("Enter month (MM format): ")
            print(f"Total Expenses for {month}: {analysis_and_visualize.total_expenses_for_month(month)}")
        elif analysis_choice == 3:
            print("Category-wise breakdown:")
            print(analysis_and_visualize.category_wise_breakdown())
        elif analysis_choice == 4:
            print("Visualizing spending by month and year...")
            analysis_and_visualize.plot_expenses_by_month_year()
        else:
            print("Invalid choice!")
    except ValueError:
        print("Invalid input! Please enter a number.")

def custom_action():
    """Allows the user to execute custom SQL commands directly."""
    conn = sqlite3.connect('finance_tracker.db')
    cursor = conn.cursor()
    
    try:
        command = input("Please enter your SQL command: ")
        cursor.execute(command)
        conn.commit()
        print("Command executed successfully!")
    except sqlite3.Error as e:
        print(f"SQL error: {e}")
    finally:
        conn.close()