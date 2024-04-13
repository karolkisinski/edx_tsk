from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ConvertedPricePLN:
    id: int
    price_in_source_currency: Decimal
    currency: str
    rate: Decimal
    date: str
    price_in_pln: Decimal
