from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from domain.stock import Stock
from infrastructure.orm.schemas import StockOrmSchema
from infrastructure.orm.session import get_db_session


class StockRepository:

    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def save(self, stock: Stock):
        stock_orm = StockOrmSchema(**stock.dict())
        self.session.add(stock_orm)
        self.session.commit()

    def bulk_update(self, stocks: List[Stock]):
        stocks_orm = [StockOrmSchema(**stock.dict()) for stock in stocks]
        for stock_orm in stocks_orm:
            self.session.merge(stock_orm)

        self.session.commit()

    def get_list_by_symbols(self, symbols: List[str]) -> List[Stock]:
        stocks_orm = self.session.query(StockOrmSchema).filter(StockOrmSchema.symbol.in_(symbols)).all()
        if not stocks_orm:
            return []
        return [Stock.from_orm(stock_orm) for stock_orm in stocks_orm]

    def get_by_symbol(self, symbol: str) -> Stock:
        stock_orm = self.session.query(StockOrmSchema).filter(StockOrmSchema.symbol == symbol).first()
        if not stock_orm:
            return None
        return Stock.from_orm(stock_orm)
