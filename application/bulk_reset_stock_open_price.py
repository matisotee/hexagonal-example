from typing import List

from fastapi import Depends

from domain.stock import Stock
from domain.stock_open_price_resetter import StockOpenPriceResetter
from infrastructure.repositories.stock import StockRepository


class BulkResetStockOpenPriceService:

    def __init__(
            self,
            stock_repository: StockRepository = Depends(StockRepository)
    ):
        self.repository = stock_repository

    def bulk_reset_stock_open_price(self, symbols: List[str]) -> Stock:
        stocks = self.repository.get_list_by_symbols(symbols)
        StockOpenPriceResetter.reset_open_price_for_stocks(stocks)
        self.repository.bulk_update(stocks)
