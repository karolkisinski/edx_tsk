from sqlalchemy import Column, Integer, String, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()


class ConvertedPricePLNSQLite(Base):
    __tablename__ = 'converted_prices'

    id = Column(Integer, primary_key=True)
    currency = Column(String)
    rate = Column(DECIMAL(10, 4))
    price_in_pln = Column(DECIMAL(10, 4))
    date = Column(Date, default=date.today)

    def _convert_to_dict(self, row):
        return {
            "id": row.id,
            "currency": row.currency,
            "rate": row.rate,
            "price_in_pln": row.price_in_pln
        }
