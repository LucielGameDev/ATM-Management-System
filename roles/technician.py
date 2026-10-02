from roles.user import User

class Technician(User):

    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)

    #Create Service:
    def view_atm_health(self):
        print("View ATM Health.")

    #Create Service:
    def schedule_atm_maintenance(self):
        print("Schedule ATM Maintenance.")

    #Create Service:
    def restart_atm_software(self):
        print("Restart ATM Software.")

    #Create Service:
    def update_atm_software(self):
        print("Update ATM Software.")

    #Create Service:
    def check_atm_cash_levels(self):
        print("Check ATM Cash Levels.")

    #Create Service:
    def refill_atm_cash(self):
        print("Refill ATM Cash.")

    #Create Service:
    def menu(self):
        while True:
            print("\n===== Technician Menu =====")
            print("1. View ATM Health")
            print("2. Schedule ATM Maintenance")
            print("3. Restart ATM Software")
            print("4. Update ATM Software")
            print("5. Check ATM Cash Levels")
            print("6. Refill ATM Cash")
            print("7. Back to Main Menu")

            option = input("\nSelect an option from the menu above: ")

            if option == "1":
                self.view_atm_health()

            elif option == "2":
                self.schedule_atm_maintenance()

            elif option == "3":
                self.restart_atm_software()

            elif option == "4":
                self.update_atm_software()

            elif option == "5":
                self.check_atm_cash_levels()

            elif option == "6":
                self.refill_atm_cash()

            elif option == "7":
                return

            else:
                print("ERROR! Invalid option. Please enter a number from 1 to 7.")