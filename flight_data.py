"""FLightData Class"""


class FlightData:
    """Class that structures the flight data"""
    def __init__(self, flight_data):
        self.price = None
        self.origin_city = None
        self.origin_airport = None
        self.destination_city = None
        self.destination_airport = None
        self.stop_overs = None
        self.via_cities = []
        self.out_date = None
        self.return_date = None
        self.url = None
        self.organize_data(flight_data)

    def organize_data(self, flight_data):
        self.price = flight_data["price"]
        self.origin_city = flight_data["cityFrom"]
        self.origin_airport = flight_data["route"][0]["flyFrom"]
        self.destination_city = flight_data["cityTo"]
        destination_airport = None
        for flight in flight_data['route']:
            if flight['cityTo'] == self.destination_city:
                destination_airport = flight['flyTo']
        self.destination_airport = destination_airport
        if len(flight_data['route']) > 2:
            self.stop_overs = int((len(flight_data['route']) - 2) / 2)
            for i in range(0, self.stop_overs):
                self.via_cities.append(flight_data['route'][0+i]['cityTo'])
        self.out_date = flight_data["route"][0]["local_departure"].split("T")[
            0]
        self.return_date = flight_data[
            "route"][1]["local_departure"].split("T")[0]
        self.url = flight_data['deep_link']
