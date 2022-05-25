"""Module for handle the kiwi API"""
import os
import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ.get("TEQUILA_KEY")


class FlightSearch:
    """Class for tequila API"""

    def get_destination_code(self, city_name):

        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers,
                                params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code,
                      from_time, to_time):
        """Check flights for some params using the Kiwi API

        Args:
            origin_city_code (str): IATAA cod for the city
            destination_city_code (str): IATAA cod for the city
            from_time (str): date in dd/mm/YYYY format
            to_time (str): date in dd/mm/YYYY format

        Returns:
            Flight Data Class: with all the params of the flight as atributes.
        """

        headers = {"apikey": TEQUILA_API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 4,
            "curr": "BRL"}
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query)
        try:
            data = response.json()["data"][0]
        except IndexError:
            return None

        flight_data = FlightData(data)

        return flight_data
