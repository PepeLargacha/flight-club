"""Main"""
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()

ORIGIN_CITY_IATA = "VIX"

for i, row in enumerate(sheet_data):
    if row["iataCode"] == "":
        data_manager.iatacode = flight_search.get_destination_code(row['city'])
        data_manager.update_destination_codes(i+2)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=180)

notification_manager = NotificationManager()
for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    try:
        if flight.price < destination["lowestPrice"]:
            data_manager.get_members()
            for row in data_manager.users:
                notification_manager.structure_msg(flight, row['email'])
    except AttributeError:
        pass

notification_manager.client.close()
