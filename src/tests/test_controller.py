import unittest
from unittest.mock import Mock
from datetime import date
from models.currency import ConvertedPricePLN
from controllers.currency_controller import PriceCurrencyConverterToPLN


class TestPriceCurrencyConverterToPLN(unittest.TestCase):
    def setUp(self):
        self.mock_db_connector = Mock()
        self.mock_source = Mock()

    def test_convert_to_pln_with_valid_data(self):
        self.mock_source.get_exchange_rate.return_value = 1.23
        self.mock_db_connector.get_max_id.return_value = 0
        converter = PriceCurrencyConverterToPLN(self.mock_db_connector,
                                                self.mock_source)
        converted_price = converter.convert_to_pln(currency="USD", price=100.0)

        expected_price = ConvertedPricePLN(
            id=1,
            price_in_source_currency=100.0,
            currency="USD",
            rate=1.23,
            price_in_pln=123.0,
            date=date.today().strftime("%Y-%m-%d")
        )

        self.mock_db_connector.save.assert_called_once_with(expected_price)
        self.assertEqual(converted_price, expected_price)

    def test_convert_to_pln_with_invalid_currency(self):
        self.mock_source.get_exchange_rate.return_value = None
        self.mock_db_connector.get_max_id.return_value = 0

        converter = PriceCurrencyConverterToPLN(self.mock_db_connector,
                                                self.mock_source)

        with self.assertRaises(ValueError):
            converter.convert_to_pln(currency="INVALID", price=100.0)


if __name__ == '__main__':
    unittest.main()
