from roles.user import User

class Customer(User):

    def __init__(self, user_id, username, password, account_number, account_balance, account_status):

        super().__init__(user_id, username, password)

        self.account_number = account_number
        self.account_balance = account_balance
        self.account_status = account_status

    #Create Service:
    def balance_inquiry(self):
        print("Balance Inquiry.")

    #Create Service:
    def withdrawal(self):
        print("Withdrawal.")

    #Create Service:
    def deposit(self):
        print("Deposit.")

    #Create Service:
    def password_change(self):
        print("Password Change.")

    #Create Service:
    def transfer_funds(self):
        print("Transfer Funds.")

    def menu(self):
        while True:
            print("\n===== Customer Menu =====")
            print("1. Balance Inquiry")
            print("2. Withdrawal")
            print("3. Deposit")
            print("4. Password Change")
            print("5. Transfer Funds")
            print("6. Back to Main Menu")

            option = input("\nSelect an option from the menu above: ")

            if option == "1":
                self.balance_inquiry()

            elif option == "2":
                self.withdrawal()

            elif option == "3":
                self.deposit()

            elif option == "4":
                self.password_change()

            elif option == "5":
                self.transfer_funds()

            elif option == "6":
                return

            else:
                print("ERROR! Invalid option. Please enter a number from 1 to 6.")