import inserting  
import analysis_and_visualize

def inserting_action():
    print("Inserting data...")
    account_id = int(input("Enter account ID: "))
    category_id = int(input("Enter category ID: "))
    amount = float(input("Enter amount: "))
    transaction_type = input("Enter transaction type (income/expense): ")
    description = input("Enter description: ")
    transaction_date = input("Enter transaction date (YYYY-MM-DD): ")
    
    inserting.insert_transaction_and_update_balance(account_id, category_id, amount, transaction_type, description, transaction_date)
    print("Transaction inserted successfully!")

def analysis_action():
    print("""
    Choose analysis:
        1 for total balance
        2 for total expenses for a month
        3 for category-wise breakdown
        4 for visualize spending by month and year
    """)
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

def main():
    while True:
        print("""
            Please choose your action:
                1 for inserting
                2 for analysis
                3 to exit
        """)
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            inserting_action()
        elif choice == 2:
            analysis_action()
        elif choice == 3:
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
