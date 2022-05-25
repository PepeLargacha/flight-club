"""Has the DataManager Class"""
import requests
import os

SHEETY_PRICES_ENDPOINT = f"{os.environ.get('SHEETY_ENDPOINT')}/prices"
SHEETY_USERS_ENDPOINT = f"{os.environ.get('SHEETY_ENDPOINT')}/users"
SHEETY_TOKEN = os.environ.get('SHEETY_TOKEN')


class DataManager:
    """ Class to manage the Sheety API """
    def __init__(self):
        self.destination_data = {}
        self.users = {}
        self.iatacode = None
        self.header = {
            'Authorization': f'Bearer {SHEETY_TOKEN}'}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT,
                                headers=self.header)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self, city_id):
        new_data = {
            "price": {
                "iataCode": self.iatacode
            }
        }
        response = requests.put(
            url=f"{SHEETY_PRICES_ENDPOINT}/{city_id}",
            json=new_data, headers=self.header,
        )
        print(response.status_code)

    def get_members(self):
        response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=self.header)
        self.users = response.json()['users']
        return True

    def insert_new_member(self, name, lastname, email):
        new_data = {
            "user": {
                'firstName': name,
                'lastName': lastname,
                'email': email,
            }
        }
        response = requests.post(url=SHEETY_USERS_ENDPOINT, json=new_data,
                                 headers=self.header)
        if response.status_code == 200:
            print('Welcome to the club')
        else:
            print(response.status_code)
