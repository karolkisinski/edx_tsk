import unittest
from unittest.mock import patch, MagicMock
from connectors.api.nbp_connector import NBPConnector


class TestNBPConnector(unittest.TestCase):

    @patch('requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': [{'mid': 4.15}]}
        mock_get.return_value = mock_response

        connector = NBPConnector()

        rate = connector.get_exchange_rate('USD')

        self.assertEqual(rate, 4.15)

    @patch('requests.get')
    def test_get_exchange_rate_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        # Response without 'mid' key
        mock_response.json.return_value = {'rates': [{}]}
        mock_get.return_value = mock_response

        connector = NBPConnector()

        with self.assertRaises(Exception):
            connector.get_exchange_rate('USD')

    @patch('requests.get')
    def test_get_exchange_rate_missing_key(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # Response without 'rates' key
        mock_get.return_value = mock_response

        connector = NBPConnector()

        with self.assertRaises(Exception):
            connector.get_exchange_rate('USD')


if __name__ == '__main__':
    unittest.main()
