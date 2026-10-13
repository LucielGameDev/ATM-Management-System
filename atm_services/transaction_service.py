from datetime import datetime

class TransactionService:

    def __init__(self, data_manager):
        self.data_manager = data_manager

    #Customer Menu (2. Withdrawal):
    def withdraw(self, account_number, amount):
        
        if amount is None or amount <= 0:
            return (False, "ERROR! Withdrawal amount must be a valid number greater than zero.")

        customer = self._find_customer(account_number)

        if customer is None:
            return (False, "ERROR! Customer not found.")

        if customer["account_status"].lower() == "frozen":
            return (False, "ERROR! Account is frozen.")

        try:
            current_balance = float(customer["account_balance"])
        except (ValueError, TypeError):
            return (False, "ERROR! Stored account balance is invalid.")

        if amount > current_balance:
            return (False, "ERROR! Insufficient funds.")

        new_balance = current_balance - amount
        
        #Keep the old balance in case saving fails:
        old_balance = customer["account_balance"]

        #Update the balance in memory:
        customer["account_balance"] = f"{new_balance:.2f}"

        #Save the updated customer data to the file:
        try:
            self.data_manager.save_customers()

            self._record_transactions([
                {
                    "transaction_type": "Withdrawal",
                    "account_number": customer["account_number"],
                    "amount": amount
                }
            ])
        except OSError:
            #Restore the original balance if saving fails:
            customer["account_balance"] = old_balance

            #Save the customer data to the file:
            try:
                self.data_manager.save_customers()
            except OSError:
                pass

            return (False, "ERROR! Could not save the withdrawal.")

        return (True, f"${amount:.2f} withdrawn successfully, your new balance is ${new_balance:.2f}.")

    
    #Customer Menu (3. Deposit):
    def deposit(self, account_number, amount):
        
        if amount is None or amount <= 0:
            return (False, "ERROR! Deposit amount must be a valid number greater than zero.")

        customer = self._find_customer(account_number)

        if customer is None:
            return (False, "ERROR! Customer not found.")

        if customer["account_status"].lower() == "frozen":
            return (False, "ERROR! Account is frozen.")

        try:
            current_balance = float(customer["account_balance"])
        except (ValueError, TypeError):
            return (False, "ERROR! Stored account balance is invalid.")

        new_balance = current_balance + amount
        
        #Keep the old balance in case saving fails:
        old_balance = customer["account_balance"]

        #Update the balance in memory:
        customer["account_balance"] = f"{new_balance:.2f}"

        #Save the updated customer data to the file:
        try:
            self.data_manager.save_customers()

            self._record_transactions([
                {
                    "transaction_type": "Deposit",
                    "account_number": customer["account_number"],
                    "amount": amount
                }
            ])
        except OSError:
            #Restore the original balance if saving fails:
            customer["account_balance"] = old_balance

            #Save the customer data to the file:
            try:
                self.data_manager.save_customers()
            except OSError:
                pass

            return (False, "ERROR! Could not save the deposit.")

        return (True, f"${amount:.2f} deposited successfully, your new balance is ${new_balance:.2f}.")


    #Customer Menu (5. Transfer Funds):
    def transfer_funds(self, sender_account_number, receiver_account_number, amount):
        if amount is None or amount <= 0:
            return (False, "ERROR! Transfer amount must be a valid number greater than zero.")

        if sender_account_number == receiver_account_number:
            return (False, "ERROR! Cannot transfer money to the same account.")

        sender = self._find_customer(sender_account_number)
        receiver = self._find_customer(receiver_account_number)
        
        if sender is None:
            return (False, "ERROR! Sender not found.")

        if receiver is None:
            return (False, "ERROR! Receiver not found.")

        if sender["account_status"].lower() == "frozen":
            return (False, "ERROR! Sender account is frozen.")

        if receiver["account_status"].lower() == "frozen":
            return (False, "ERROR! Receiver account is frozen.")

        try:
            sender_balance = float(sender["account_balance"])
        except (ValueError, TypeError):
            return (False, "ERROR! Sender stored account balance is invalid.")

        try:
            receiver_balance = float(receiver["account_balance"])
        except (ValueError, TypeError):
            return (False, "ERROR! Receiver stored account balance is invalid.")
        
        if amount > sender_balance:
            return (False, "ERROR! Insufficient funds.")

        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver_balance + amount

        #Keep the original balances in case saving fails:
        old_sender_balance = sender["account_balance"]
        old_receiver_balance = receiver["account_balance"]

        #Update both balances in memory.
        sender["account_balance"] = f"{new_sender_balance:.2f}"
        receiver["account_balance"] = f"{new_receiver_balance:.2f}"

        timestamp = datetime.now().isoformat(timespec="seconds")

        #Save the updated customers data to the file:
        try:
            self.data_manager.save_customers()

            #Record both sides of the transfer:
            self._record_transactions([
                {
                    "transaction_type": "Transfer",
                    "account_number": sender["account_number"],
                    "amount": amount,
                    "related_account": receiver["account_number"],
                    "timestamp": timestamp
                },
                {
                    "transaction_type": "Transfer",
                    "account_number": receiver["account_number"],
                    "amount": amount,
                    "related_account": sender["account_number"],
                    "timestamp": timestamp
                }
            ])
        except OSError:
            #Restore both balances if saving fails:
            sender["account_balance"] = old_sender_balance
            receiver["account_balance"] = old_receiver_balance

            #Save the customers data to the file:
            try:
                self.data_manager.save_customers()
            except OSError:
                pass

            return (False, "ERROR! Could not save the transfer.")

        return (True, f"${amount:.2f} transferred successfully, your new balance is ${new_sender_balance:.2f}.")


    #Admin Menu (6. View Customer Transactions History):
    def view_customer_transactions(self, account_number):
        
        customer = self._find_customer(account_number)

        if customer is None:
            return (False, "ERROR! Customer account not found.", None)
        
        #Retrieve the transaction history for the specified account number:
        history = [
            #Create a copy of the transaction to avoid modifying the original data:
            transaction.copy()
            for transaction in self.data_manager.transactions
            if transaction["account_number"] == account_number
        ]

        return (True, "Transaction history retrieved successfully.", history)


    #Admin Menu (7. View Transactions Logs):
    def view_transaction_logs(self):
        
        logs = [
            #Create a copy of the transaction to avoid modifying the original data:
            transaction.copy()
            for transaction in self.data_manager.transactions
        ]

        return (True, "Transaction logs retrieved successfully.", logs)


    #Find a customer by their account number:
    def _find_customer(self, account_number):

        for customer in self.data_manager.customers:
            if customer["account_number"] == account_number:
                return customer

        return None


    #Generate a unique transaction ID:
    def _generate_transaction_id(self):

        #If there are no existing transactions, start with "TRX000001":
        if not self.data_manager.transactions:
            return "TRS000001"

        highest_number = 0

        #Iterate through existing transactions to find the highest transaction ID number:
        for transaction in self.data_manager.transactions:
            transaction_id = transaction["transaction_id"]

            #Check if the transaction ID starts with "TRS":
            if transaction_id.startswith("TRS"):

                #Extract the numeric part of the transaction ID and update the highest number found:
                try:
                    number = int(transaction_id[3:])
                    highest_number = max(highest_number, number)
                except ValueError:
                    #If the numeric part is not a valid integer, skip this transaction ID and continue to the next one:
                    continue

        #Generate the next transaction ID by incrementing the highest number found and formatting it with leading zeros:
        return f"TRS{highest_number + 1:06d}"


    #Records Transactions:
    def _record_transaction(self, transaction_type, account_number, amount, related_account=None, timestamp=None):
        
        #Generate a unique transaction ID for the new transaction:
        transaction_id = self._generate_transaction_id()
        
        if timestamp is None:
            timestamp = datetime.now().isoformat(timespec="seconds")

        transaction = {
            "transaction_id": transaction_id,
            "transaction_type": transaction_type,
            "account_number": account_number,
            "amount": f"{amount:.2f}",
            "related_account": related_account,
            "timestamp": timestamp
        }

        #Add the transaction record to memory:
        self.data_manager.transactions.append(transaction)

        #Save the transaction record to the file:
        try:
            self.data_manager.save_transactions()
        except OSError:
            #Remove the transaction from memory if saving fails:
            self.data_manager.transactions.remove(transaction)
            #Raise an exception to the service to indicate that the transaction record could not be saved:
            raise