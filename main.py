import actions

def main():
    while True:
        print("""
            Please choose your action:
                1 for inserting
                2 for analysis
                3 for custom SQL command
                4 to exit
        """)
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            actions.inserting_action()
        elif choice == 2:
            actions.analysis_action()
        elif choice == 3:
            actions.custom_action()
        elif choice == 4:
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
