import requests


class IATAFinder:
    def __init__(self):
        self.API_KEY = "#####"
        self.IATA_KIWI_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
        self.header = {
                "apikey": self.API_KEY
            }

    def find(self, text: str):
        try:
            para = {
                "term": text
            }
            send = requests.get(url=self.IATA_KIWI_ENDPOINT, headers=self.header, params=para)
            data = send.json()
            IATA = data["locations"][0]["code"]
            return IATA
        except IndexError:
            IATA = "notfound"
            return IATA
