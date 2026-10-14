from roles.customer import Customer
from roles.admin import Admin
from roles.technician import Technician
from hashing_passwords import verify_password

class AuthenticationService:

    def __init__(self, data_manager):
        self.data_manager = data_manager

    #Customer Authentication (Login):
    def authenticate_customer(self, user_id, password):
        
        for customer_data in self.data_manager.customers:

            if customer_data["user_id"] == user_id:

                if not verify_password(password, customer_data["password"]):
                    return (False, "ERROR! Incorrect password.", None)

                if customer_data["account_status"].lower() == "frozen":
                    return (False, "ERROR! Account is frozen.", None)

                customer = Customer(
                    user_id=customer_data["user_id"],
                    username=customer_data["username"],
                    password=customer_data["password"],
                    account_number=customer_data["account_number"],
                    account_balance=float(customer_data["account_balance"]),
                    account_status=customer_data["account_status"]
                )

                return (True, "Login successful.", customer)

        return (False, "ERROR! User ID not found.", None)

    #Admin Authentication (Login):
    def authenticate_admin(self, user_id, password):
        
        for admin_data in self.data_manager.admins:

            if admin_data["user_id"] == user_id:

                if not verify_password(password, admin_data["password"]):
                    return (False, "ERROR! Incorrect password.", None)

                admin = Admin(
                    user_id=admin_data["user_id"],
                    username=admin_data["username"],
                    password=admin_data["password"]
                )

                return (True, "Login successful.", admin)

        return (False, "ERROR! User ID not found.", None)

    #Technician Authentication (Login):
    def authenticate_technician(self, user_id, password):
        
        for technician_data in self.data_manager.technicians:

            if technician_data["user_id"] == user_id:

                if not verify_password(password, technician_data["password"]):
                    return (False, "ERROR! Incorrect password.", None)

                technician = Technician(
                    user_id=technician_data["user_id"],
                    username=technician_data["username"],
                    password=technician_data["password"]
                )

                return (True, "Login successful.", technician)

        return (False, "ERROR! User ID not found.", None)