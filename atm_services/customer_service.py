class CustomerService:

    def __init__(self, data_manager):
        self.data_manager = data_manager

    #Customer Menu (1. Balance Inquiry):
    def balance_inquiry(self, user_id):
        
        customer = self._find_customer(user_id)
        
        if customer is None:
            return (False, "ERROR! Customer not found.", None)
        
        return (True, "Balance retrieved successfully.", float(customer["account_balance"]))

    #Customer Menu (4. Password Change):
    def change_customer_password(self, user_id, current_password, new_password):
        
        customer = self._find_customer(user_id)
        
        if customer is None:
            return (False, "ERROR! Customer not found.")
        
        if customer["password"] != current_password:
            return (False, "ERROR! Current password is incorrect.")
        
        if not new_password:
            return (False, "ERROR! Password cannot be empty.")
        
        if any(character.isspace() for character in new_password):
            return (False, "ERROR! Password cannot contain spaces.")

        if new_password == current_password:
            return (False, "ERROR! New password must differ from the current password.")

        #Keep the original password in case saving fails:
        old_password = customer["password"]

        #Update the password in memory:
        customer["password"] = new_password

        #Save the updated password to the file:
        try:
            self.data_manager.save_customers()
        except OSError:
            #Restore the old password if saving fails:
            customer["password"] = old_password
            return (False, "ERROR! Could not save the password change.")

        return (True, "Password changed successfully.")

    #Admin Menu (1. Create Customer Account):
    def create_customer_account(self, user_id, username, password, account_number, account_balance):
        
        if any(customer["user_id"] == user_id for customer in self.data_manager.customers):
            return (False, "ERROR! User ID already exists.")

        if any(customer["account_number"] == account_number for customer in self.data_manager.customers):
            return (False, "ERROR! Account number already exists.")

        #Validate the required information:
        if not all([user_id, username, password, account_number]):
            return (False, "ERROR! All customer details are required.")

        #Convert account balance to float and validate it:
        try:
            balance = float(account_balance)
        except (ValueError, TypeError):
            return (False, "ERROR! Account balance must be a valid number.")

        if balance < 0:
            return (False, "ERROR! Account balance cannot be negative.")

        #Create the customer record:
        customer = {
            "user_id": user_id,
            "username": username,
            "password": password,
            "account_number": account_number,
            "account_balance": f"{balance:.2f}",
            "account_status": "Active"
        }

        #Add the customer record to memory:
        self.data_manager.customers.append(customer)

        #Save the customer record to the file:
        try:
            self.data_manager.save_customers()
        except OSError:
            #Remove the customer from memory if saving fails:
            self.data_manager.customers.remove(customer)
            return (False, "ERROR! Could not save the customer account.")

        return (True, "Customer account created successfully.")

    #Admin Menu (2. Delete Customer Account):
    def delete_customer_account(self, user_id):
        
        customer = self._find_customer(user_id)

        if customer is None:
            return (False, "ERROR! Customer not found.")

        #Keep the data in case saving fails:
        customer_index = self.data_manager.customers.index(customer)

        #Remove the customer data from memory:
        self.data_manager.customers.pop(customer_index)

        #Save the updated customer data to the file:
        try:
            self.data_manager.save_customers()
        except OSError:
            #Restore the customer data if saving fails:
            self.data_manager.customers.insert(customer_index, customer)
            return (False, "ERROR! Could not save the customer records.")

        return (True, "Customer account deleted successfully.")

    #Admin Menu (3. Modify Customer Information):
    def modify_customer_information(self, user_id, new_username, new_password):
        
        customer = self._find_customer(user_id)

        if customer is None:
            return (False, "ERROR! Customer not found.")

        #Validate and prepare any requested changes first:
        updates = {}

        #Reject an empty string or a string containing only spaces:
        if new_username is not None:
            if not new_username.strip():
                return (False, "ERROR! Username cannot be empty.")
            
            updates["username"] = new_username.strip()

        #Reject both an empty string and a string containing spaces:
        if new_password is not None:
            if not new_password:
                return (False, "ERROR! Password cannot be empty.")

            if any(character.isspace() for character in new_password):
                return (False, "ERROR! Password cannot contain spaces.")

            updates["password"] = new_password

        #Check if there are any changes:
        if not updates:
            return (False, "ERROR! No changes were provided.")

        #Keep the original values so we can restore them if saving fails:
        original_values = {field: customer[field] for field in updates}

        #Update the customer data in memory:
        customer.update(updates)

        #Save the customer data updates to the file:
        try:
            self.data_manager.save_customers()
        except OSError:
            #Restore the original values if saving fails:
            customer.update(original_values)
            return (False, "ERROR! Could not save the customer changes.")

        return (True, "Customer information updated successfully.")

    #Admin Menu (4. View Customer Account Information):
    def view_customer_account_info(self, user_id):
        
        customer = self._find_customer(user_id)

        #Check if customer exists:
        if customer is None:
            return (False, "ERROR! Customer not found.", None)

        #Return a copy so that callers cannot accidentally change stored data:
        return (True, "Customer account information retrieved successfully", customer.copy())

    #Admin Menu (5. Change Customer Account Status):
    def change_customer_account_status(self, user_id, new_status):
        
        customer = self._find_customer(user_id)

        if customer is None:
            return (False, "ERROR! Customer not found.")

        normalized_status = new_status.strip().lower()

        if normalized_status not in ("active", "frozen"):
            return (False, "ERROR! Status must be Active or Frozen.")

        #Use consistent capitalization in the data file:
        new_status = normalized_status.capitalize()

        #Keep the old status in case saving fails:
        old_status = customer["account_status"]

        #Check if the status was not changed:
        if old_status == new_status:
            return (False, f"Account is already {new_status.lower()}.")

        #Update the account status in memory:
        customer["account_status"] = new_status

        #Save the updated account status to the file:
        try:
            self.data_manager.save_customers()
        except OSError:
            #Restore the old status if saving fails:
            customer["account_status"] = old_status
            return (False, "ERROR! Could not save the account status.")

        return (True, f"Customer account status was changed to {new_status.lower()} successfully.")

    #Find a customer by their user ID:
    def _find_customer(self, user_id):

        for customer in self.data_manager.customers:
            if customer["user_id"] == user_id:
                return customer

        return None