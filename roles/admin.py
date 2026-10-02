from roles.user import User

class Admin(User):

    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)

    #Create Service:
    def create_customer_account(self):
        print("Create Customer Account.")

    #Create Service:
    def delete_customer_account(self):
        print("Delete Customer Account.")

    #Create Service:
    def modify_customer_information(self):
        print("Modify Customer Information.")

    #Create Service:
    def view_customer_accounts(self):
        print("View Customer Accounts.")

    #Create Service:
    def freeze_customer_account(self):
        print("Freeze Customer Account.")

    #Create Service:
    def unfreeze_customer_account(self):
        print("Unfreeze Customer Account.")

    #Create Service:
    def view_customer_transactions(self):
        print("View Customer Transactions History.")

    #Create Service:
    def view_transaction_logs(self):
        print("View Transactions Logs.")

    def menu(self):
        while True:
            print("\n======= Admin Menu =======")
            print("1. Create Customer Account")
            print("2. Delete Customer Account")
            print("3. Modify Customer Information")
            print("4. View Customer Accounts")
            print("5. Freeze Customer Account")
            print("6. Unfreeze Customer Account")
            print("7. View Customer Transactions History")
            print("8. View Transactions Logs")
            print("9. Back to Main Menu")

            option = input("\nSelect an option from the menu above: ")

            if option == "1":
                self.create_customer_account()

            elif option == "2":
                self.delete_customer_account()

            elif option == "3":
                self.modify_customer_information()

            elif option == "4":
                self.view_customer_accounts()

            elif option == "5":
                self.freeze_customer_account()

            elif option == "6":
                self.unfreeze_customer_account()

            elif option == "7":
                self.view_customer_transactions()

            elif option == "8":
                self.view_transaction_logs()

            elif option == "9":
                return

            else:
                print("ERROR! Invalid option. Please enter a number from 1 to 9.")