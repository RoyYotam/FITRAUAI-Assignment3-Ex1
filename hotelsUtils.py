from datetime import datetime
from enum import Enum
import serpapi
# just for test!!! todo delete this
import json


class SerpapiType(Enum):
    HOTELS = 1
    FLIGHTS = 2


class SerpapiUtils:
    def __init__(self, from_date: datetime, to_date: datetime):
        self.from_date = None
        self.to_date = None

        self.set_time(from_date, to_date)

    def set_time(self, from_date: datetime, to_date: datetime):
        self.from_date = from_date
        self.to_date = to_date

    def get_time(self) -> {}:
        times = {}
        from_date_str = self.from_date.strftime('%Y-%m-%d')
        to_date_str = self.to_date.strftime('%Y-%m-%d')
        times['from_date'] = from_date_str
        times['to_date'] = to_date_str
        return times

    def plan_trip_hotel_flight(self, where_to: [{}], budget: int):
        results = []

        for location in where_to:
            if 'Airport_code' not in location or 'Place' not in location:
                continue

            from_flight = self.search(SerpapiType.FLIGHTS, budget, location['Airport_code'])

            if from_flight == {}:
                continue

            from_flight_token = self.get_token_from_flight(from_flight)

            if from_flight_token == "":
                continue

            to_flight = self.search(SerpapiType.HOTELS, budget, location['Airport_code'], from_flight_token)

            if to_flight == {}:
                continue

            flights_price = self.get_price_from_flight(from_flight)

            if flights_price == -1:
                continue

            hotel = self.search(SerpapiType.HOTELS, (budget - flights_price), location['Place'])

            if hotel == {}:
                continue

            result = {
                'hotel': hotel,
                'from_flight': from_flight,
                'to_flight': to_flight
            }

            results.append(result)

        return results

    def search(self, request_type: SerpapiType, budget: int, where_to: str, flight_token: str = None):
        times = self.get_time()

        if request_type == SerpapiType.HOTELS:
            return self.get_hotel(where_to, times, budget)
        elif request_type == SerpapiType.FLIGHTS:
            return self.get_flight(where_to, times, budget, flight_token)
        else:
            return {}

    @staticmethod
    def get_flight(where_to: str, times: {}, budget: int, flight_token: str):
        try:
            params = {
                "engine": "google_flights",
                "departure_id": "TLV",
                "arrival_id": where_to,
                "hl": "en",
                "gl": "us",
                "currency": "USD",
                "outbound_date": times['from_date'],
                "return_date": times['to_date'],
                "api_key": "MY_KEY_HERE"
            }

            if flight_token:
                params['departure_token'] = flight_token

            search = serpapi.search(params)
            results = search.as_dict()

            return SerpapiUtils.get_lowest_price_flight(results, budget)

        except Exception as _:
            return {}

    @staticmethod
    def get_hotel(where_to: str, times: {}, budget: int):
        try:
            params = {
                "engine": "google_hotels",
                "q": where_to,
                "check_in_date": times['from_date'],
                "check_out_date": times['to_date'],
                "gl": "us",
                "hl": "en",
                "currency": "USD",
                "adults": "1",
                "max_price": budget,
                "api_key": "MY_KEY_HERE"
            }

            search = serpapi.search(params)
            results = search.as_dict()

            return SerpapiUtils.get_max_affordable_price_hotel(results, budget)

        except Exception as _:
            return {}

    # @staticmethod
    # def load_from_file():
    #     # Reading the dictionary from the file
    #     with open('hotels_data.txt', 'r') as file:
    #         loaded_results = json.load(file)
    #         print(SerpapiUtils.get_max_affordable_price_hotel(loaded_results, 800))
    #
    # @staticmethod
    # def load_from_file2():
    #     # Reading the dictionary from the file
    #     with open('from_flight_data_3.txt', 'r') as file:
    #         loaded_results = json.load(file)
    #         print(SerpapiUtils.get_lowest_price_flight(loaded_results, 800))
    #
    # @staticmethod
    # def load_from_file3():
    #     # Reading the dictionary from the file
    #     with open('from_flight_data_3.txt', 'r') as file:
    #         loaded_results = json.load(file)
    #         res = SerpapiUtils.get_lowest_price_flight(loaded_results, 800)
    #         print(res)

    @staticmethod
    def get_max_affordable_price_hotel(hotels_data: {}, budget: int) -> {}:
        max_affordable_price_hotel = {}
        price_for_max_affordable_price_hotel = 0

        try:
            hotels = hotels_data['properties']

            for hotel in hotels:
                price = hotel['total_rate']['extracted_lowest']
                if budget >= price > price_for_max_affordable_price_hotel:
                    price_for_max_affordable_price_hotel = price
                    max_affordable_price_hotel = hotel

        except Exception as _:
            pass

        return max_affordable_price_hotel

    @staticmethod
    def get_lowest_price_flight(flights_data: {}, budget: int) -> {}:
        lowest_price_flight = {}
        price_for_lowest_price_flight = budget

        try:
            best_flights = []
            other_flights = []

            if 'best_flights' in flights_data:
                best_flights = flights_data['best_flights']

            if 'other_flights' in flights_data:
                other_flights = flights_data['other_flights']

            for flight in best_flights + other_flights:
                price = flight['price']
                if price <= price_for_lowest_price_flight:
                    price_for_lowest_price_flight = price
                    lowest_price_flight = flight

        except Exception as _:
            pass

        return lowest_price_flight

    @staticmethod
    def get_token_from_flight(flight_data: {}) -> str:
        token = ""
        try:
            token = flight_data['departure_token']
        except Exception as _:
            pass
        return token

    @staticmethod
    def get_price_from_flight(flight_data: {}) -> int:
        price = -1
        try:
            price = int(flight_data['price'])
        except Exception as _:
            pass
        return price


if __name__ == "__main__":
    serpapi_utils = SerpapiUtils(datetime(2024, 6, 20), datetime(2024, 6, 25))
    # serpapi_utils.search(SerpapiType.HOTELS, 800, where_to="Phuket, Thailand")
    # serpapi_utils.load_from_file()
    # serpapi_utils.search(SerpapiType.FLIGHTS, 800, where_to="HKT")
    # serpapi_utils.load_from_file2()
    # token = "WyJDalJJUlhCS1lreGtlRXRhUkZWQlRHWmFhVUZDUnkwdExTMHRMUzB0TFhCbVozTXhNMEZCUVVGQlIxcE1iV2RWVFdSS09HTkJFZ3RCU1RFME1IeEJTVE0zTmhvTENMSDNBeEFDR2dOVlUwUTRISEN4OXdNPSIsW1siVExWIiwiMjAyNC0wNi0yMCIsIkRFTCIsbnVsbCwiQUkiLCIxNDAiXSxbIkRFTCIsIjIwMjQtMDYtMjEiLCJIS1QiLG51bGwsIkFJIiwiMzc2Il1dXQ=="
    # serpapi_utils.search(SerpapiType.FLIGHTS, 800, where_to="HKT", flight_token=token)
    # serpapi_utils.load_from_file3()

