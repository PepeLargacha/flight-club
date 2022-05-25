"""UI Module to get user info"""
from data_manager import DataManager


class NewMember:
    """ Data form the new members """
    def __init__(self, manager: DataManager) -> None:
        self.manager = manager
        self.first_name = None
        self.last_name = None
        self.email = None
        self.get_user_info()

    def get_user_info(self):
        self.first_name = input("What's your first name?\n")
        self.last_name = input("What's your last name?\n")
        self.email = self.get_email()

    def get_email(self):
        self.email = input("Type your e-mail adress:\n")
        confirm_email = input("Please, confirm your e-mail:\n")
        if self.email == confirm_email and all([self.email is not None,
                                                self.email != ""]):
            self.manager.insert_new_member(
                self.first_name, self.last_name, self.email)
            return self.email

        else:
            print("e-mail doesn't match or is empty. Please type again.")
            return self.get_email()


manager = DataManager()
ui = NewMember(manager)
