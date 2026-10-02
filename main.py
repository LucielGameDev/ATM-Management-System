from roles.customer import Customer
from roles.admin import Admin
from roles.technician import Technician

def main():
    while True:
        print("\n===== ATM Management System =====")
        print("1. Customer")
        print("2. Admin")
        print("3. Technician")
        print("4. Exit")

        option = input("\nSelect an option from the menu above: ")

        if option == "1":
            customer = Customer()
            customer.menu()

        elif option == "2":
            admin = Admin()
            admin.menu()

        elif option == "3":
            technician = Technician()
            technician.menu()

        elif option == "4":
            print("Thank you for using the ATM Management System.")
            break

        else:
            print("ERROR! Invalid option. Please enter a number from 1 to 4.")


if __name__ == "__main__":
    main()