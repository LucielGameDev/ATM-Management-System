from datetime import datetime

class TransactionService:

    def __init__(self):
        self.transactions = []
        self.next_transaction_id = 1

    #Customer Menu (2. Withdrawal):
    def withdraw(self, customer, amount):
        if amount <= 0:
            return False, "ERROR! Withdrawal amount must be greater than zero."

        if customer.account_status.lower() == "frozen":
            return False, "ERROR! Account is frozen."

        if amount > customer.account_balance:
            return False, "ERROR! Insufficient funds."

        customer.account_balance -= amount

        self._record_transaction(
            transaction_type = "Withdrawal",
            account_number = customer.account_number,
            amount = amount
        )

        return True, f"${amount:.2f} withdrawn successfully."

    
    #Customer Menu (3. Deposit):
    def deposit(self, customer, amount):
        if amount <= 0:
            return False, "ERROR! Deposit amount must be greater than zero."

        if customer.account_status.lower() == "frozen":
            return False, "ERROR! Account is frozen."

        customer.account_balance += amount

        self._record_transaction(
            transaction_type = "Deposit",
            account_number = customer.account_number,
            amount = amount
        )

        return True, f"${amount:.2f} deposited successfully."


    #Customer Menu (5. Transfer Funds):
    def transfer_funds(self, sender, receiver, amount):
        if amount <= 0:
            return False, "ERROR! Transfer amount must be greater than zero."

        if sender.account_status.lower() == "frozen":
            return False, "ERROR! Sender account is frozen."

        if receiver.account_status.lower() == "frozen":
            return False, "ERROR! Receiver account is frozen."

        if sender.account_number == receiver.account_number:
            return False, "ERROR! Cannot transfer money to the same account."

        if amount > sender.account_balance:
            return False, "ERROR! Insufficient funds."

        sender.account_balance -= amount
        receiver.account_balance += amount

        timestamp = datetime.now()

        self._record_transaction(
            transaction_type = "Transfer",
            account_number = sender.account_number,
            amount = amount,
            related_account = receiver.account_number,
            timestamp = timestamp
        )

        self._record_transaction(
            transaction_type = "Transfer",
            account_number = receiver.account_number,
            amount = amount,
            related_account = sender.account_number,
            timestamp = timestamp
        )

        return True, f"${amount:.2f} transferred successfully."


    #Admin Menu (6. View Customer Transactions History):
    def view_customer_transactions(self, account_number):
        history = []

        for transaction in self.transactions:
            if transaction["account_number"] == account_number:
                history.append(transaction)

        return history


    #Admin Menu (7. View Transactions Logs):
    def view_transaction_logs(self):
        return self.transactions


    #Records Transactions (Will store later):
    def _record_transaction(self, transaction_type, account_number, amount, related_account=None, timestamp=None):
        
        if timestamp is None:
            timestamp = datetime.now()

        transaction = {
            "transaction_id": self.next_transaction_id,
            "transaction_type": transaction_type,
            "account_number": account_number,
            "amount": amount,
            "related_account": related_account,
            "timestamp": timestamp
        }

        self.transactions.append(transaction)
        self.next_transaction_id += 1