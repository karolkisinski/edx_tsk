from models.currency import ConvertedPricePLN
from datetime import date


class PriceCurrencyConverterToPLN:
    def __init__(self, db_connector, source):
        self.db_connector = db_connector
        self.source = source

    def convert_to_pln(self, *,
                       currency: str,
                       price: float) -> ConvertedPricePLN:
        currency_rate = self.source.get_exchange_rate(currency)
        new_id = self.db_connector.get_max_id() + 1
        if currency_rate is None:
            raise ValueError(f"{currency} not found.")
        converted_price = ConvertedPricePLN(
                                        id=new_id,
                                        price_in_source_currency=price,
                                        currency=currency,
                                        rate=currency_rate,
                                        price_in_pln=price*currency_rate,
                                        date=date.today().strftime("%Y-%m-%d"))
        self.db_connector.save(converted_price)
        return converted_price
