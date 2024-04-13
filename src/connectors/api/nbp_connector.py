import requests
from exceptions.exceptions import NBPAPIError
from config import NBP_API_URL


class NBPConnector:
    def __init__(self):
        self.base_url = NBP_API_URL

    def get_exchange_rate(self, code: str) -> float:
        try:
            response = requests.get(self.base_url.format(code))
            response.raise_for_status()
            data = response.json()
            rate = data['rates'][0]['mid']
            return rate
        except requests.RequestException as e:
            raise NBPAPIError(f"Error fetching exchange rate from NBP API: {e}") # noqa
