import actions

# Main program loop
def main():
    while True:
        print("""
        Choose your action:
            1 for inserting data
            2 for analysis
            3 for custom SQL command
            4 to exit
        """)
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                actions.inserting_action()
            elif choice == 2:
                actions.analysis_action()
            elif choice == 3:
                actions.custom_action()
            elif choice == 4:
                print("Exiting the program... Goodbye!")
                break
            else:
                print("Invalid choice! Please choose between 1 and 4.")
        except ValueError:
            print("Invalid input! Please enter a number.")

if __name__ == "__main__":
    main()
