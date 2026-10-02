from roles.customer import Customer
from roles.admin import Admin
from roles.technician import Technician

class AuthenticationService:

    #Customer Authentication (Login):
    def authenticate_customer(self, user_id, password):
        try:
            with open("data/customers.txt", "r") as file:

                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    data = line.split(",")

                    stored_user_id = data[0]
                    username = data[1]
                    stored_password = data[2]
                    account_number = data[3]
                    account_balance = float(data[4])
                    account_status = data[5]

                    if stored_user_id == user_id:

                        if stored_password != password:
                            return (False, "ERROR! Incorrect password.", None)

                        if account_status.lower() == "frozen":
                            return (False, "ERROR! Account is frozen.", None)

                        customer = Customer(user_id, username, password, account_number, account_balance, account_status)

                        return (True, "Login successful.", customer)

            return (False, "ERROR! User ID not found.", None)

        except FileNotFoundError:
            return (False, "ERROR! customers.txt not found.", None)


    #Admin Authentication (Login):
    def authenticate_admin(self, user_id, password):
        try:
            with open("data/admins.txt", "r") as file:

                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    data = line.split(",")

                    stored_user_id = data[0]
                    username = data[1]
                    stored_password = data[2]

                    if stored_user_id == user_id:

                        if stored_password != password:
                            return (False, "ERROR! Incorrect password.", None)

                        admin = Admin(user_id, username, password)

                        return (True, "Login successful.", admin)

            return (False, "ERROR! User ID not found.", None)

        except FileNotFoundError:
            return (False, "ERROR! admins.txt not found.", None)


    #Technician Authentication (Login):
    def authenticate_technician(self, user_id, password):
        try:
            with open("data/technicians.txt", "r") as file:

                for line in file:
                    line = line.strip()

                    if not line:
                        continue

                    data = line.split(",")

                    stored_user_id = data[0]
                    username = data[1]
                    stored_password = data[2]

                    if stored_user_id == user_id:

                        if stored_password != password:
                            return (False, "ERROR! Incorrect password.", None)

                        technician = Technician(user_id, username, password)

                        return (True, "Login successful.", technician)

            return (False, "ERROR! User ID not found.", None)

        except FileNotFoundError:
            return (False, "ERROR! technicians.txt not found.", None)