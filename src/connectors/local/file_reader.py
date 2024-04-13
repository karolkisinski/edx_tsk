import json
from typing import Optional
from datetime import date
from exceptions.exceptions import RateForDateNotFound, RatesFileNotFound, RatesDataInvalid, RatesReadError # noqa


class LocalFileDataSource:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._read_data()

    def _read_data(self) -> dict:
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise RatesFileNotFound("Rates data file not found.")
        except json.JSONDecodeError:
            raise RatesDataInvalid("Invalid JSON format in rates data file.")
        except Exception as e:
            raise RatesReadError(f"Error reading rates data from file: {e}")

    def get_exchange_rate(self, currency: str) -> Optional[float]:
        rates = self.data.get(currency)
        current_date = date.today().strftime("%Y-%m-%d")
        if rates:
            for rate_entry in rates:
                if rate_entry['date'] == current_date:
                    return rate_entry['rate']
        raise RateForDateNotFound(f"No rate found for currency {currency} on date {current_date}") # noqa
