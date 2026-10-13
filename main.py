from data_manager import DataManager

from atm_services.authentication import AuthenticationService
from atm_services.atm_service import ATMService
from atm_services.customer_service import CustomerService
from atm_services.transaction_service import TransactionService

#Main Menu:
def main():

    #Initialize and load the application's data:
    data_manager = DataManager()
    data_manager.load_data()

    #Initialize all services:
    authentication_service = AuthenticationService(data_manager)
    atm_service = ATMService(data_manager)
    customer_service = CustomerService(data_manager)
    transaction_service = TransactionService(data_manager)

    while True:
        print("\n===== ATM Management System =====")
        print("1. Customer")
        print("2. Admin")
        print("3. Technician")
        print("4. Exit")

        option = input("\nSelect an option from the menu above: ").strip()

        if option == "1":
            login_customer(authentication_service, customer_service, transaction_service)

        elif option == "2":
            login_admin(authentication_service, customer_service, transaction_service)

        elif option == "3":
            login_technician(authentication_service, atm_service)

        elif option == "4":
            print("Thank you for using the ATM Management System.")
            break

        else:
            print("ERROR! Invalid option. Please enter a number from 1 to 4.")


def login_customer(authentication_service, customer_service, transaction_service):
    print("\n===== Customer Login =====")

    user_id = input("Enter User ID: ").strip()
    password = input("Enter Password: ")

    success, message, customer = (authentication_service.authenticate_customer(user_id, password))

    print(f"\n{message}")

    if success:
        customer.menu(customer_service, transaction_service)


def login_admin(authentication_service, customer_service, transaction_service):
    print("\n===== Admin Login =====")

    user_id = input("Enter User ID: ").strip()
    password = input("Enter Password: ")

    success, message, admin = (authentication_service.authenticate_admin(user_id, password))

    print(f"\n{message}")

    if success:
        admin.menu(customer_service, transaction_service)


def login_technician(authentication_service, atm_service):
    print("\n===== Technician Login =====")

    user_id = input("Enter User ID: ").strip()
    password = input("Enter Password: ")

    success, message, technician = (authentication_service.authenticate_technician(user_id, password))

    print(f"\n{message}")

    if success:
        technician.menu(atm_service)


if __name__ == "__main__":
    main()