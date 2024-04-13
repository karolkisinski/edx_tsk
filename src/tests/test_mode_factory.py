import unittest
from unittest.mock import Mock
from controllers.currency_controller import PriceCurrencyConverterToPLN
from connectors.database.json import JsonFileDatabaseConnector
from connectors.local.file_reader import LocalFileDataSource
from exceptions.exceptions import InvalidAmountError
from handlers.mode_factory import HandlerFactory
from connectors.api.nbp_connector import NBPConnector
from connectors.database.sqlite import SQLLiteConnector


class TestDevModeHandler(unittest.TestCase):
    def setUp(self):
        self.mock_local_source = Mock(spec=LocalFileDataSource)
        self.mock_db_connector = Mock(spec=JsonFileDatabaseConnector)
        self.mock_converter = Mock(spec=PriceCurrencyConverterToPLN)

        self.handler = HandlerFactory.create_handler('dev')
        self.handler.local_source = self.mock_local_source
        self.handler.db_connector = self.mock_db_connector
        self.handler.converter = self.mock_converter

    def test_process_with_valid_data(self):
        self.mock_local_source.get_exchange_rate.return_value = 1.23
        self.mock_converter.convert_to_pln.return_value = None

        self.handler.process(currency="USD", amount="100.0")

        self.mock_converter.convert_to_pln.assert_called_once_with(
            currency="USD", price=100.0)

    def test_process_with_negative_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.handler.process(currency="USD", amount="-100.0")

    def test_process_with_invalid_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.handler.process(currency="USD", amount="invalid")


class TestProdModeHandler(unittest.TestCase):
    def setUp(self):
        self.mock_db_connector = Mock(spec=SQLLiteConnector)
        self.mock_nbp_connector = Mock(spec=NBPConnector)
        self.mock_converter = Mock(spec=PriceCurrencyConverterToPLN)

        self.handler = HandlerFactory.create_handler('prod')
        self.handler.db_connector = self.mock_db_connector
        self.handler.nbp = self.mock_nbp_connector
        self.handler.converter = self.mock_converter

    def test_process_with_valid_data(self):
        self.mock_converter.convert_to_pln.return_value = None

        self.handler.process(currency="USD", amount="100.0")

        self.mock_converter.convert_to_pln.assert_called_once_with(
            currency="USD", price=100.0)

    def test_process_with_negative_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.handler.process(currency="USD", amount="-100.0")

    def test_process_with_invalid_amount(self):
        with self.assertRaises(InvalidAmountError):
            self.handler.process(currency="USD", amount="invalid")


if __name__ == '__main__':
    unittest.main()
