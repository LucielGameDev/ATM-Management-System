from user import User
class Technician(User):
    def __init__(self, account_number, pin):
        super().__init__(account_number, pin)