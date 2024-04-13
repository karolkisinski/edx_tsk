import os
import json
import unittest
from models.currency import ConvertedPricePLN
from connectors.database.json import JsonFileDatabaseConnector
from datetime import date


class TestJsonFileDatabaseConnector(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_database.json"
        with open(self.test_db_path, "w") as file:
            json.dump({}, file)

        self.connector = JsonFileDatabaseConnector(self.test_db_path)

    def tearDown(self):
        os.remove(self.test_db_path)

    def test_save_and_get_by_id(self):
        entity = ConvertedPricePLN(
            id=None,
            price_in_source_currency=100,
            currency="EUR",
            rate=4.15,
            price_in_pln=415.0,
            date=date.today().strftime("%Y-%m-%d")
        )

        entity_id = self.connector.save(entity)

        retrieved_entity = self.connector.get_by_id(entity_id)

        self.assertEqual(retrieved_entity, {
            "id": None,
            "currency": "EUR",
            "rate": 4.15,
            "date": date.today().strftime("%Y-%m-%d"),
            "price_in_pln": 415.0,
        })

    def test_get_all(self):
        self.assertEqual(len(self.connector.get_all()), 0)

        entity1 = ConvertedPricePLN(
            id=1,
            price_in_source_currency=100,
            currency="EUR",
            rate=4.15,
            price_in_pln=415.0,
            date=date.today().strftime("%Y-%m-%d")
        )
        entity2 = ConvertedPricePLN(
            id=2,
            price_in_source_currency=150,
            currency="USD",
            rate=3.50,
            price_in_pln=525.0,
            date=date.today().strftime("%Y-%m-%d")
        )
        self.connector.save(entity1)
        self.connector.save(entity2)

        all_entities = self.connector.get_all()

        self.assertEqual(len(all_entities), 2)
