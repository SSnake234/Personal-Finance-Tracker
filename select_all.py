import sqlite3

def list_categories():
    conn = sqlite3.connect('finance_tracker.db')  # Connect to your database
    cursor = conn.cursor()
    
    # Query to list all rows from the Categories table
    cursor.execute("SELECT * FROM Accounts;")
    
    # Fetch and print all rows from the Categories table
    categories = cursor.fetchall()
    print("Categories in the database:")
    for category in categories:
        print(category)  # Prints the entire row of each category
    
    conn.close()

# Example usage
list_categories()
