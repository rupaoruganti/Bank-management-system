from bank import BankManagement

def main_menu():
    print("\n=== Bank Management System ===")
    print("1. Create New Customer")
    print("2. Create New Account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Check Balance")
    print("6. Transaction History")
    print("7. Exit")
    return input("Choose an option (1-7): ")

def main():
    bank = BankManagement()
    
    while True:
        choice = main_menu()
        
        if choice == '1':
            print("\n=== Create New Customer ===")
            name = input("Enter customer name: ")
            address = input("Enter address: ")
            phone = input("Enter phone number: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            
            if bank.create_customer(name, address, phone, email, password):
                print("Customer created successfully!")
            else:
                print("Failed to create customer.")

        elif choice == '2':
            print("\n=== Create New Account ===")
            customer_id = int(input("Enter customer ID: "))
            account_type = input("Enter account type (savings/current): ")
            initial_balance = float(input("Enter initial balance: "))
            
            if bank.create_account(customer_id, account_type, initial_balance):
                print("Account created successfully!")
            else:
                print("Failed to create account.")

        elif choice == '3':
            print("\n=== Deposit Money ===")
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to deposit: "))
            
            if bank.deposit(account_id, amount):
                print("Deposit successful!")
            else:
                print("Deposit failed.")

        elif choice == '4':
            print("\n=== Withdraw Money ===")
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to withdraw: "))
            
            if bank.withdraw(account_id, amount):
                print("Withdrawal successful!")
            else:
                print("Withdrawal failed.")

        elif choice == '5':
            print("\n=== Check Balance ===")
            account_id = int(input("Enter account ID: "))
            balance = bank.check_balance(account_id)
            
            if balance is not None:
                print(f"Current balance: ${balance:.2f}")
            else:
                print("Could not retrieve balance.")

        elif choice == '6':
            print("\n=== Transaction History ===")
            account_id = int(input("Enter account ID: "))
            transactions = bank.get_transaction_history(account_id)
            
            if transactions:
                print("\nTransaction History:")
                for transaction in transactions:
                    print(f"ID: {transaction[0]}")
                    print(f"Type: {transaction[2]}")
                    print(f"Amount: ${transaction[3]:.2f}")
                    print(f"Date: {transaction[5]}")
                    print("-" * 30)
            else:
                print("No transactions found.")

        elif choice == '7':
            print("Thank you for using the Bank Management System!")
            bank.close_connection()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()