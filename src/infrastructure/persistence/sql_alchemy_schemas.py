from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session


Base = declarative_base()


class StockOrmSchema(Base):
    __tablename__ = 'stock'

    symbol = Column(String, primary_key=True, index=True)
    open_price = Column(String)
    higher_price = Column(String)
    lower_price = Column(String)
    variation = Column(String)
