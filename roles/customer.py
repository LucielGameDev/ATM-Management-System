from roles.user import User

class Customer(User):

    def __init__(self, user_id, username, password, account_number, account_balance, account_status):

        super().__init__(user_id, username, password)

        self.account_number = account_number
        self.account_balance = account_balance
        self.account_status = account_status

    #Create Service:
    def balance_inquiry(self, customer_service):
        
        success, message, balance = (customer_service.balance_inquiry(self.user_id))
        
        print(message)

        if success:
            print(f"Current balance: ${balance:.2f}")

    #Create Service:
    def withdrawal(self, transaction_service):
        
        amount = input("Enter withdrawal amount: ").strip()

        success, message = transaction_service.withdraw(self.account_number, amount)

        print(message)

    #Create Service:
    def deposit(self, transaction_service):
        
        amount = input("Enter deposit amount: ").strip()

        success, message = transaction_service.deposit(self.account_number, amount)

        print(message)

    #Create Service:
    def change_customer_password(self, customer_service):
        
        current_password = input("Enter current password: ")
        new_password = input("Enter new password: ")

        success, message = (customer_service.change_customer_password(self.user_id, current_password, new_password))

        print(message)

        if success:
            self.password = new_password

    #Create Service:
    def transfer_funds(self, transaction_service):
        
        receiver_account_number = input("Enter receiver's account number: ").strip()

        amount = input("Enter transfer amount: ").strip()

        success, message = transaction_service.transfer_funds(self.account_number, receiver_account_number, amount)

        print(message)

    def menu(self, customer_service, transaction_service):
        while True:
            print("\n===== Customer Menu =====")
            print("1. Balance Inquiry")
            print("2. Withdrawal")
            print("3. Deposit")
            print("4. Password Change")
            print("5. Transfer Funds")
            print("6. Back to Main Menu")

            option = input("\nSelect an option from the menu above: ").strip()

            if option == "1":
                self.balance_inquiry(customer_service)

            elif option == "2":
                self.withdrawal(transaction_service)

            elif option == "3":
                self.deposit(transaction_service)

            elif option == "4":
                self.change_customer_password(customer_service)

            elif option == "5":
                self.transfer_funds(transaction_service)

            elif option == "6":
                print("Returning to the main menu...")
                return

            else:
                print("ERROR! Invalid option. Please enter a number from 1 to 6.")