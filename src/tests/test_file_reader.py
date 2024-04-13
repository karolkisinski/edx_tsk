import unittest
from datetime import date
from unittest.mock import mock_open, patch
from connectors.local.file_reader import LocalFileDataSource
from exceptions.exceptions import RateForDateNotFound, RatesFileNotFound, RatesDataInvalid, RatesReadError # noqa
import json


class TestLocalFileDataSource(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "USD": [{"date": date.today().strftime("%Y-%m-%d"), "rate": 1.23}],
            "EUR": [{"date": date.today().strftime("%Y-%m-%d"), "rate": 0.89}]
        }

    def test_init_with_valid_data(self):
        with patch("builtins.open", new_callable=mock_open,
                   read_data=json.dumps(self.valid_data)):
            data_source = LocalFileDataSource("valid_rates.json")
            self.assertEqual(data_source.filename, "valid_rates.json")
            self.assertEqual(data_source.data, self.valid_data)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_init_with_missing_file(self, mock_open):
        with self.assertRaises(RatesFileNotFound):
            LocalFileDataSource("nonexistent_file.json")

    @patch("builtins.open", side_effect=json.JSONDecodeError("", "", 0))
    def test_init_with_invalid_json(self, mock_open):
        with self.assertRaises(RatesDataInvalid):
            LocalFileDataSource("invalid_data.json")

    @patch("builtins.open", side_effect=Exception("Something went wrong"))
    def test_init_with_generic_error(self, mock_open):
        with self.assertRaises(RatesReadError):
            LocalFileDataSource("generic_error.json")

    def test_get_exchange_rate_valid(self):
        with patch("builtins.open", new_callable=mock_open,
                   read_data=json.dumps(self.valid_data)):
            data_source = LocalFileDataSource("valid_rates.json")
            self.assertEqual(data_source.get_exchange_rate("USD"), 1.23)
            self.assertEqual(data_source.get_exchange_rate("EUR"), 0.89)

    def test_get_exchange_rate_invalid_currency(self):
        with patch("builtins.open", new_callable=mock_open,
                   read_data=json.dumps(self.valid_data)):
            data_source = LocalFileDataSource("valid_rates.json")
            with self.assertRaises(RateForDateNotFound):
                data_source.get_exchange_rate("XXX")

    def test_get_exchange_rate_invalid_date(self):
        invalid_data = {
            "USD": [{"date": "2024-04-09", "rate": 1.23}]
        }
        with patch("builtins.open", new_callable=mock_open,
                   read_data=json.dumps(invalid_data)):
            data_source = LocalFileDataSource("valid_rates.json")
            with self.assertRaises(RateForDateNotFound):
                data_source.get_exchange_rate("USD")


if __name__ == '__main__':
    unittest.main()
