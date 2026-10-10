from pathlib import Path
import csv


class DataManager:

    def __init__(self):

        self.data_directory = Path(__file__).parent / "data"

        self.customers_file = self.data_directory / "customers.txt"
        self.admins_file = self.data_directory / "admins.txt"
        self.technicians_file = self.data_directory / "technicians.txt"
        self.atm_config_file = self.data_directory / "atm_config.txt"
        self.transactions_file = self.data_directory / "transactions.txt"

        # Shared data stored in memory:
        self.customers = []
        self.admins = []
        self.technicians = []
        self.atm_config = []
        self.transactions = []

 #---------------------------------------------------LOADING DATA---------------------------------------------------
    
    #Load all persistent data into memory:
    def load_data(self):

        #Load from customers.txt:
        self.customers = self._load_records(
            self.customers_file,
            ["user_id", "username", "password", "account_number", "account_balance", "account_status"]
        )

        #Load from admins.txt:
        self.admins = self._load_records(
            self.admins_file,
            ["user_id", "username", "password"]
        )

        #Load from technicians.txt:
        self.technicians = self._load_records(
            self.technicians_file,
            ["user_id", "username", "password"]
        )

        #Load from transactions.txt:
        self.transactions = self._load_records(
            self.transactions_file,
            ["transaction_id", "transaction_type", "account_number", "amount", "related_account", "timestamp"]
        )

        #Load from atm_config.txt:
        self.atm_config = self._load_records(
            self.atm_config_file,
            ["atm_id", "software_version", "last_maintenance_date", "atm_status", "cash_level"]
        )

        atm_ids = [atm["atm_id"] for atm in self.atm_config]

        if len(set(atm_ids)) != len(atm_ids):
            raise ValueError("ERROR! Each ATM must have a unique ATM ID.")

    #Load a CSV-style file into a list of dictionaries:
    def _load_records(self, file_path, fields):

        records = []

        if not file_path.exists():
            raise FileNotFoundError(f"ERROR! Required data file not found: {file_path}")

        with file_path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            for line_number, row in enumerate(reader, start=1):
                if not row:
                    continue

                #Check that the number of values in the row matches the number of expected fields:
                if len(row) != len(fields):
                    raise ValueError(
                        f"ERROR! Invalid record in {file_path.name}, "
                        f"line {line_number}: expected "
                        f"{len(fields)} fields, found {len(row)}."
                    )

                #Pair each field with its corresponding value, then turn those pairs into a dictionary:
                record = dict(zip(fields, row))
                #Add the dictionary to records:
                records.append(record)

        return records

 #---------------------------------------------------SAVING DATA---------------------------------------------------
    
    #Save customer data to customers.txt:
    def save_customers(self):

        self._save_records(
            self.customers_file,
            self.customers,
            ["user_id", "username", "password", "account_number", "account_balance", "account_status"]
        )

    #Save admin data to admins.txt:
    def save_admins(self):

        self._save_records(
            self.admins_file,
            self.admins,
            ["user_id", "username", "password"]
        )

    #Save technician data to technicians.txt:
    def save_technicians(self):

        self._save_records(
            self.technicians_file,
            self.technicians,
            ["user_id", "username", "password"]
        )

    #Save transaction records to transactions.txt:
    def save_transactions(self):

        self._save_records(
            self.transactions_file,
            self.transactions,
            ["transaction_id", "transaction_type", "account_number", "amount", "related_account", "timestamp"]
        )

    #Save all ATM configurations:
    def save_atm_config(self):

        self._save_records(
            self.atm_config_file,
            self.atm_config,
            ["atm_id", "software_version", "last_maintenance_date", "atm_status", "cash_level"]
        )

    #Write dictionaries to a CSV-style text file:
    def _save_records(self, file_path, records, fields):

        #Create a temporary file path (if file is customers.txt, temporary file will be customers.txt.tmp):
        temporary_file = file_path.with_suffix(file_path.suffix + ".tmp")

        with temporary_file.open("w", newline="", encoding="utf-8") as file:
            
            #Prepare to write comma-separated rows:
            writer = csv.writer(file)

            for record in records:
                writer.writerow([record[field] for field in fields])

        #Replace the original file after writing completes:
        temporary_file.replace(file_path)