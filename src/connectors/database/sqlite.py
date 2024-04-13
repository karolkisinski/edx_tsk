from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.currency_sqlite import Base, ConvertedPricePLNSQLite # noqa
from models.currency import ConvertedPricePLN
import os
import json


class SQLLiteConnector():
    def __init__(self):
        database_path = os.path.join(os.getcwd(), "database.db")
        self.engine = create_engine(f"sqlite:///{database_path}")

        Base.metadata.create_all(self.engine)

    def _convert_to_dict(self, row):
        return {
            "id": row.id,
            "currency": row.currency,
            "rate": row.rate,
            "price_in_pln": row.price_in_pln
        }

    def get_max_id(self):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            max_id = session.query(ConvertedPricePLNSQLite.id).order_by(
                ConvertedPricePLNSQLite.id.desc()).first()
            return max_id[0] if max_id else 0

    def save(self, converted_price: ConvertedPricePLN):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            converted_price_model = ConvertedPricePLNSQLite(
                currency=converted_price.currency,
                rate=converted_price.rate,
                price_in_pln=converted_price.price_in_pln)

            session.add(converted_price_model)
            session.commit()

    def get_all(self) -> json:
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            data = session.query(ConvertedPricePLNSQLite).all()
            converted_data = {str(row.id): self._convert_to_dict(row)
                              for row in data}
            return json.dumps(converted_data)

    def get_by_id(self, id):
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            data = session.query(ConvertedPricePLNSQLite
                                 ).filter_by(id=id).first()
            return {str(data.id): self._convert_to_dict(data)}
