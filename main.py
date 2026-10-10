from data_manager import DataManager
from atm_services.authentication import AuthenticationService

#Main Menu:
def main():

    #Initialize and load the application's data:
    data_manager = DataManager()
    data_manager.load_data()

    #Initialize the authentication service:
    authentication_service = AuthenticationService(data_manager)

    while True:
        print("\n===== ATM Management System =====")
        print("1. Customer")
        print("2. Admin")
        print("3. Technician")
        print("4. Exit")

        option = input("\nSelect an option from the menu above: ")

        if option == "1":
            login_customer(authentication_service)

        elif option == "2":
            login_admin(authentication_service)

        elif option == "3":
            login_technician(authentication_service)

        elif option == "4":
            print("Thank you for using the ATM Management System.")
            break

        else:
            print("ERROR! Invalid option. Please enter a number from 1 to 4.")


def login_customer(authentication_service):
    print("\n===== Customer Login =====")

    user_id = input("Enter User ID: ")
    password = input("Enter Password: ")

    success, message, customer = (authentication_service.authenticate_customer(user_id, password))

    print(f"\n{message}")

    if success:
        customer.menu()


def login_admin(authentication_service):
    print("\n===== Admin Login =====")

    user_id = input("Enter User ID: ")
    password = input("Enter Password: ")

    success, message, admin = (authentication_service.authenticate_admin(user_id, password))

    print(f"\n{message}")

    if success:
        admin.menu()


def login_technician(authentication_service):
    print("\n===== Technician Login =====")

    user_id = input("Enter User ID: ")
    password = input("Enter Password: ")

    success, message, technician = (authentication_service.authenticate_technician(user_id, password))

    print(f"\n{message}")

    if success:
        technician.menu()


if __name__ == "__main__":
    main()