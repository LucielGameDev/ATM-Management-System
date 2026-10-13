from roles.user import User

class Technician(User):

    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password)

    #1. View ATM Health:
    def view_atm_health(self, atm_service):
        
        print("\n===== VIEW ATM HEALTH =====")

        atm_id = input("Enter ATM ID: ").strip()

        success, message, report = atm_service.view_atm_health(atm_id)

        print(message)

        if success:
            print("\n----- ATM Health Report -----")
            print(f"ATM ID: {report['atm_id']}")
            print(f"ATM Status: {report['atm_status']}")
            print(f"Software Version: {report['software_version']}")
            print(f"Last Maintenance Date: {report['last_maintenance_date']}")
            print(f"Scheduled Maintenance Date: {report['scheduled_maintenance_date']}")
            print(f"Cash Level: ${float(report['cash_level']):.2f}")

    #2. Schedule ATM Maintenance:
    def schedule_atm_maintenance(self, atm_service):
        
        print("\n===== SCHEDULE ATM MAINTENANCE =====")

        atm_id = input("Enter ATM ID: ").strip()
        maintenance_date = input("Enter scheduled maintenance date (YYYY-MM-DD): ").strip()

        success, message = atm_service.schedule_atm_maintenance(atm_id, maintenance_date)

        print(message)

    #3. Restart ATM Software:
    def restart_atm_software(self, atm_service):
        
        print("\n===== RESTART ATM SOFTWARE =====")

        atm_id = input("Enter ATM ID: ").strip()

        confirmation = input(f"Restart software for {atm_id}? (y/n): ").strip().lower()

        if confirmation != "y":
            print("Software restart cancelled.")
            return

        success, message = atm_service.restart_atm_software(atm_id)

        print(message)

    #4. Update ATM Software:
    def update_atm_software(self, atm_service):
        
        print("\n===== UPDATE ATM SOFTWARE =====")

        atm_id = input("Enter ATM ID: ").strip()
        new_version = input("Enter new software version: ").strip()

        success, message = atm_service.update_atm_software(atm_id, new_version)

        print(message)

    #5. Check ATM Cash Levels:
    def check_atm_cash_levels(self, atm_service):
        
        print("\n===== CHECK ATM CASH LEVELS =====")

        atm_id = input("Enter ATM ID: ").strip()

        success, message, cash_level = (atm_service.check_atm_cash_levels(atm_id))

        print(message)

        if success:
            print(f"Current cash level: ${float(cash_level):.2f}")

    #6. Refill ATM Cash:
    def refill_atm_cash(self, atm_service):
        
        print("\n===== REFILL ATM CASH =====")

        atm_id = input("Enter ATM ID: ").strip()
        amount = input("Enter refill amount: ").strip()

        success, message = atm_service.refill_atm_cash(atm_id, amount)

        print(message)

    def menu(self, atm_service):
        while True:
            print("\n===== Technician Menu =====")
            print("1. View ATM Health")
            print("2. Schedule ATM Maintenance")
            print("3. Restart ATM Software")
            print("4. Update ATM Software")
            print("5. Check ATM Cash Levels")
            print("6. Refill ATM Cash")
            print("7. Back to Main Menu")

            option = input("\nSelect an option from the menu above: ").strip()

            if option == "1":
                self.view_atm_health(atm_service)

            elif option == "2":
                self.schedule_atm_maintenance(atm_service)

            elif option == "3":
                self.restart_atm_software(atm_service)

            elif option == "4":
                self.update_atm_software(atm_service)

            elif option == "5":
                self.check_atm_cash_levels(atm_service)

            elif option == "6":
                self.refill_atm_cash(atm_service)

            elif option == "7":
                print("Returning to the main menu...")
                return

            else:
                print("ERROR! Invalid option. Please enter a number from 1 to 7.")