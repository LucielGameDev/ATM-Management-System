from roles.user import User

class Admin(User):

    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)

    #1. Create Customer Account:
    def create_customer_account(self, customer_service):
        
        print("\n===== CREATE CUSTOMER ACCOUNT =====")

        user_id = input("Enter new customer user ID: ").strip()
        username = input("Enter username: ").strip()
        password = input("Enter password: ")
        account_number = input("Enter account number: ").strip()
        initial_balance = input("Enter initial balance (press Enter for 0): ").strip()

        if not initial_balance:
            initial_balance = 0.0

        success, message = customer_service.create_customer_account(
            user_id,
            username,
            password,
            account_number,
            initial_balance
        )

        print(message)

    #2. Delete Customer Account:
    def delete_customer_account(self, customer_service):
        
        print("\n===== DELETE CUSTOMER ACCOUNT =====")

        user_id = input("Enter the user ID of the customer to delete: ").strip()

        confirmation = input(f"Are you sure you want to delete customer {user_id}? (y/n): ").strip().lower()

        if confirmation != "y":
            print("Account deletion cancelled.")
            return

        success, message = customer_service.delete_customer_account(user_id)

        print(message)

    #3. Modify Customer Information:
    def modify_customer_information(self, customer_service):
        
        print("\n===== MODIFY CUSTOMER INFORMATION =====")

        user_id = input("Enter the user ID of the customer to modify their information: ").strip()

        print("Leave a field empty if you do not want to change it.")

        new_username = input("Enter customer new username: ").strip()
        new_password = input("Enter customer new password: ")

        if not new_username and not new_password:
            print("ERROR! No changes were entered.")
            return

        #Convert empty inputs to None so they are not changed.
        if not new_username:
            new_username = None

        if not new_password:
            new_password = None

        success, message = customer_service.modify_customer_information(user_id, new_username=new_username, new_password=new_password)

        print(message)

    #4. View Customer Account Information:
    def view_customer_account_info(self, customer_service):
        
        print("\n===== VIEW CUSTOMER ACCOUNT INFORMATION =====")

        user_id = input("Enter the user ID of the customer: ").strip()

        success, message, customer = (customer_service.view_customer_account_info(user_id))

        print(message)

        if success:
            print("\n===== Customer Information =====\n")
            print(f"User ID: {customer['user_id']}")
            print(f"Username: {customer['username']}")
            print(f"Account Number: {customer['account_number']}")
            print(f"Account Balance: ${float(customer['account_balance']):.2f}")
            print(f"Account Status: {customer['account_status']}")

    #5. Change Customer Account Status:
    def change_customer_account_status(self, customer_service):
        
        print("\n===== CHANGE CUSTOMER ACCOUNT STATUS =====")

        user_id = input("Enter the user ID of the customer: ").strip()

        new_status = input("Enter the new account status (Active/Frozen): ").strip()

        success, message = customer_service.change_customer_account_status(user_id, new_status)

        print(message)

    #6. View Customer Transaction History:
    def view_customer_transactions(self, transaction_service):
        
        print("\n===== VIEW CUSTOMER TRANSACTION HISTORY =====")

        account_number = input("Enter the customer's account number: ").strip()

        success, message, history = (transaction_service.view_customer_transactions(account_number))

        print(message)

        if success:
            self._display_transactions(history)

    #7. View Transaction Logs:
    def view_transaction_logs(self, transaction_service):
        print("\n===== VIEW TRANSACTION LOGS =====")

        success, message, logs = (transaction_service.view_transaction_logs())

        print(message)

        if success:
            self._display_transactions(logs)

    def menu(self, customer_service, transaction_service):

        while True:
            print("\n======= Admin Menu =======")
            print("1. Create Customer Account")
            print("2. Delete Customer Account")
            print("3. Modify Customer Information")
            print("4. View Customer Account Information")
            print("5. Change Customer Account Status")
            print("6. View Customer Transaction History")
            print("7. View Transaction Logs")
            print("8. Back to Main Menu")

            option = input("\nSelect an option from the menu above: ").strip()

            if option == "1":
                self.create_customer_account(customer_service)

            elif option == "2":
                self.delete_customer_account(customer_service)

            elif option == "3":
                self.modify_customer_information(customer_service)

            elif option == "4":
                self.view_customer_account_info(customer_service)

            elif option == "5":
                self.change_customer_account_status(customer_service)

            elif option == "6":
                self.view_customer_transactions(transaction_service)

            elif option == "7":
                self.view_transaction_logs(transaction_service)

            elif option == "8":
                print("Returning to the main menu...")
                return

            else:
                print("ERROR! Invalid option. Please enter a number from 1 to 8.")

    @staticmethod
    def _display_transactions(transactions):
        
        if not transactions:
            print("No transactions found.\n")
            return

        for transaction in transactions:
            print("\n---------------------------------------------\n")
            print(f"Transaction ID: {transaction['transaction_id']}")
            print(f"Transaction Type: {transaction['transaction_type']}")
            print(f"Account Number: {transaction['account_number']}")
            print(f"Amount: ${float(transaction['amount']):.2f}")

            related_account = transaction["related_account"]

            if related_account:
                print(f"Related Account: {related_account}")

            print(f"Timestamp: {transaction['timestamp']}")