import json
import os
from dataclasses import asdict
from models.currency import ConvertedPricePLN


class JsonFileDatabaseConnector:
    def __init__(self, db_path) -> None:
        self.db_path = db_path
        # Initialize with empty dictionary if file doesn't exist
        if not os.path.exists(db_path):
            with open(db_path, 'w') as file:
                json.dump({}, file)
        self._data = self._read_data()

    def _read_data(self) -> dict:
        with open(self.db_path, "r") as file:
            return json.load(file)

    def save(self, entity: ConvertedPricePLN) -> int:
        entity_dict = asdict(entity)
        entity_id = entity.id

        self._data[str(entity_id)] = entity_dict

        # Remove unnecessary field
        entity_dict.pop("price_in_source_currency")

        with open(self.db_path, 'w') as file:
            json.dump(self._data, file, indent=2)

        return entity_id

    def get_all(self) -> list[dict]:
        return list(self._data.values())

    def get_by_id(self, id) -> dict:
        return self._data.get(str(id), None)

    def get_max_id(self) -> int:
        return max(map(int, self._data.keys()), default=0)
