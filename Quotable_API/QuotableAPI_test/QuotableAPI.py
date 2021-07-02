import requests
import json


class QuotableAPI:

    def __init__(self):
        self.API_endpoint = "https://api.quotable.io/quotes"

    def getQuotes(self, params=None):
        response = requests.get(self.API_endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to get the quotes with the required parameters")
            return None

