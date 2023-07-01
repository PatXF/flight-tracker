import requests
from datetime import *


class DataManager:
    def __init__(self):
        self.API_KEY = "#####"
        self.KIWI_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
        self.date_from = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
        self.date_to = (date.today() + timedelta(days=180)).strftime("%d/%m/%Y")
        self.sheety_endpoint_get = "https://api.sheety.co/ebe6533ebeca0ea09b7256f6fe3d64b3/flightData/sheet1"
        self.sheety_header = {
            "Authorization": "####"
        }
        sheety_response = requests.get(url=self.sheety_endpoint_get, headers=self.sheety_header)
        self.data = sheety_response.json()
        self.header = {
            "apikey": self.API_KEY
        }

    def get_data(self, i):
        from_date = self.date_from
        to_date = self.date_to
        min_price = self.data["sheet1"][i]["min"]
        para = {
            "fly_from": self.data["sheet1"][i]["from"],
            "fly_to": self.data["sheet1"][i]["to"],
            "date_from": from_date,
            "date_to": to_date,
            "curr": "INR"
        }
        response = requests.get(url=self.KIWI_ENDPOINT, params=para, headers=self.header)
        kiwi_data = response.json()
        lowest_price = kiwi_data["data"][0]["price"]
        number = self.data["sheet1"][i]["number"]
        from_loc = self.data["sheet1"][i]["from"]
        to_loc = self.data["sheet1"][i]["to"]
        depart = kiwi_data["data"][0]["route"][0]["local_departure"]
        link = kiwi_data["data"][0]["deep_link"]
        depart = depart.split("T")
        depart_date = depart[0]
        depart_time = (depart[1].split("."))[0]
        try:
            output = {
                "price": lowest_price,
                "date": depart_date,
                "time": depart_time,
                "number": number,
                "from": from_loc,
                "to": to_loc,
                "link": link
            }
            if int(lowest_price) < int(min_price):
                return output

        except TypeError:
            return
