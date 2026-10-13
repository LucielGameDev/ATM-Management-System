from datetime import date, datetime

class ATMService:

    def __init__(self, data_manager):
        self.data_manager = data_manager

    #Technician Menu (1. View ATM Health):
    def view_atm_health(self, atm_id):
        
        atm = self._find_atm(atm_id)
        
        if atm is None:
            return (False, "ERROR! ATM not found.", None)
        
        health_report = {
            "atm_id": atm["atm_id"],
            "atm_status": atm["atm_status"],
            "software_version": atm["software_version"],
            "last_maintenance_date": (
                atm["last_maintenance_date"]
                if atm["last_maintenance_date"]
                else "No maintenance recorded"
                ),
            "scheduled_maintenance_date": (
                atm["scheduled_maintenance_date"]
                if atm["scheduled_maintenance_date"]
                else "No maintenance scheduled"
                ),
            "cash_level": atm["cash_level"]
        }
        
        return (True, "ATM health report retrieved successfully.", health_report)

    #Technician Menu (2. Schedule ATM Maintenance):
    def schedule_atm_maintenance(self, atm_id, maintenance_date):
        
        atm = self._find_atm(atm_id)

        if atm is None:
            return (False, "ERROR! ATM not found.")

        #Validate the maintenance date format:
        try:
            scheduled_date = date.fromisoformat(maintenance_date)
        except (ValueError, TypeError):
            return (False, "ERROR! Enter a valid date in YYYY-MM-DD format.")

        if scheduled_date < date.today():
            return (False, "ERROR! Maintenance date cannot be in the past.")

        #Keep the old date in case saving fails:
        old_date = atm["scheduled_maintenance_date"]

        #Update the scheduled maintenance date in memory:
        atm["scheduled_maintenance_date"] = scheduled_date.isoformat()

        #Save the updated scheduled maintenance date to the file:
        try:
            self.data_manager.save_atm_config()
        except OSError:
            #Restore the old date if saving fails:
            atm["scheduled_maintenance_date"] = old_date
            return (False, "ERROR! Could not save the maintenance schedule.")

        return (True, "ATM maintenance scheduled successfully.")

    #Technician Menu (3. Restart ATM Software):
    def restart_atm_software(self, atm_id):
        
        atm = self._find_atm(atm_id)

        if atm is None:
            return (False, "ERROR! ATM not found.")

        #Keep the old status in case saving fails:
        old_status = atm["atm_status"]

        #Update the ATM status to "Restarting" in memory:
        atm["atm_status"] = "Restarting"

        #Save the updated ATM status to the file:
        try:
            self.data_manager.save_atm_config()
        except OSError:
            #Restore the old status if saving fails:
            atm["atm_status"] = old_status
            return (False, "ERROR! Could not save the ATM status.")

        #This is just a simulation; it does not restart physical hardware.
        #Update the ATM status in memory:
        atm["atm_status"] = "Operational"

        #Save the final ATM status to the file:
        try:
            self.data_manager.save_atm_config()
        except OSError:
            #Restore the old status if saving fails:
            atm["atm_status"] = old_status
            return (False, "ERROR! Restart simulation failed to save its final status.")

        return (True, "ATM software restart simulated successfully.")

    #Technician Menu (4. Update ATM Software):
    def update_atm_software(self, atm_id, new_version):
        
        atm = self._find_atm(atm_id)

        if atm is None:
            return (False, "ERROR! ATM not found.")

        #Reject an empty string or a string containing only spaces:
        if not new_version or not new_version.strip():
            return (False, "ERROR! Software version cannot be empty.")

        new_version = new_version.strip()
        
        #Keep the old version in case saving fails:
        old_version = atm["software_version"]

        if new_version == old_version:
            return (False, "ERROR! ATM is already using that software version.")

        #Update the software version in memory:
        atm["software_version"] = new_version

        #Save the updated software version to the file:
        try:
            self.data_manager.save_atm_config()
        except OSError:
            #Restore the old version if saving fails:
            atm["software_version"] = old_version
            return (False, "ERROR! Could not save the software version.")

        #This is just a simulation; no software is actually installed.
        return (True, f"Software update simulated. Version is now {new_version}.")

    #Technician Menu (5. Check ATM Cash Levels):
    def check_atm_cash_levels(self, atm_id):
        
        atm = self._find_atm(atm_id)

        if atm is None:
            return (False, "ERROR! ATM not found.", None)

        #Validate that the cash level is a valid number:
        try:
            cash_level = float(atm["cash_level"])
        except (ValueError, TypeError):
            return (False, "ERROR! ATM cash level contains invalid data.", None)

        return (True, "ATM cash level retrieved successfully.", cash_level)

    #Technician Menu (6. Refill ATM Cash):
    def refill_atm_cash(self, atm_id, amount):
        
        atm = self._find_atm(atm_id)

        if atm is None:
            return (False, "ERROR! ATM not found.")

        #Validate that the refill amount and current cash level are valid numbers:
        try:
            refill_amount = float(amount)
            current_cash = float(atm["cash_level"])
        except (ValueError, TypeError):
            return (False, "ERROR! Cash amounts must be valid numbers.")

        if refill_amount <= 0:
            return (False, "ERROR! Refill amount must be greater than zero.")

        #Keep the old cash level in case saving fails:
        old_cash_level = atm["cash_level"]
        new_cash_level = current_cash + refill_amount

        #Update the cash level in memory:
        atm["cash_level"] = f"{new_cash_level:.2f}"

        #Save the updated cash level to the file:
        try:
            self.data_manager.save_atm_config()
        except OSError:
            #Restore the old cash level if saving fails:
            atm["cash_level"] = old_cash_level
            return (False, "ERROR! Could not save the updated cash level.")

        return (True, f"ATM refilled successfully. New cash level: "f"{new_cash_level:.2f}.")

    #Find an ATM by its ID:
    def _find_atm(self, atm_id):

        for atm in self.data_manager.atm_config:
            if atm["atm_id"] == atm_id:
                return atm

        return None