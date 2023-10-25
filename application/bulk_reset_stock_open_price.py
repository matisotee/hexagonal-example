from importlib import import_module
from typing import List

from fastapi import Depends

from domain.repositories.stock_repository import StockRepositoryBase
from domain.stock import Stock
from domain.stock_open_price_resetter import StockOpenPriceResetter


class BulkResetStockOpenPriceService:

    def __init__(
            self,
            stock_repository: StockRepositoryBase = Depends(getattr(import_module('infrastructure.repositories.stock'), 'StockRepository'))
    ):
        self.repository = stock_repository

    def bulk_reset_stock_open_price(self, symbols: List[str]) -> Stock:
        stocks = self.repository.get_list_by_symbols(symbols)
        StockOpenPriceResetter.reset_open_price_for_stocks(stocks)
        self.repository.bulk_update(stocks)
