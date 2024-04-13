from abc import ABC, abstractmethod
from controllers.currency_controller import PriceCurrencyConverterToPLN
from connectors.database.sqlite import SQLLiteConnector
from connectors.api.nbp_connector import NBPConnector
from connectors.local.file_reader import LocalFileDataSource
from exceptions.exceptions import InvalidAmountError, InvalidModeError
from config import JSON_DATABASE_NAME, LOCAL_SOURCE_FILE
from connectors.database.json import JsonFileDatabaseConnector


class Handler(ABC):
    @abstractmethod
    def process(self, currency, amount):
        pass


class DevModeHandler(Handler):
    def __init__(self):
        local_source = LocalFileDataSource(LOCAL_SOURCE_FILE)
        db_connector = JsonFileDatabaseConnector(JSON_DATABASE_NAME)
        converter = PriceCurrencyConverterToPLN(db_connector, local_source)
        self.converter = converter

    def process(self, currency, amount):
        try:
            amount_float = float(amount)
            if amount_float < 0:
                raise InvalidAmountError("Amount must be non-negative.")
            self.converter.convert_to_pln(currency=currency.upper(),
                                          price=amount_float)
        except ValueError:
            raise InvalidAmountError("Amount must be a valid number.")


class ProdModeHandler(Handler):
    def __init__(self):
        db_connector = SQLLiteConnector()
        nbp = NBPConnector()
        converter = PriceCurrencyConverterToPLN(db_connector, nbp)
        self.converter = converter

    def process(self, currency, amount):
        try:
            amount_float = float(amount)
            if amount_float < 0:
                raise InvalidAmountError("Amount must be non-negative.")
            self.converter.convert_to_pln(currency=currency.upper(),
                                          price=amount_float)
        except ValueError:
            raise InvalidAmountError("Amount must be a valid number.")


class HandlerFactory:
    @staticmethod
    def create_handler(mode: str):
        handler_class_name = f"{mode.capitalize()}ModeHandler"
        handler_class = globals().get(handler_class_name)

        if handler_class:
            return handler_class()
        else:
            raise InvalidModeError("Invalid mode | Available modes: dev/prod")
