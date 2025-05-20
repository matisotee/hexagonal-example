from typing import List

from src.domain.services.stock_open_price_resetter import StockOpenPriceResetter
from src.domain.unit_of_work import SyncUnitOfWork


class BulkResetStockOpenPriceService:

    def __init__(self, uow: SyncUnitOfWork):
        self.uow = uow

    def bulk_reset_stock_open_price(self, symbols: List[str]):
        with self.uow:
            stocks = self.uow.stock_repo.get_list_by_symbols(symbols)
            StockOpenPriceResetter.reset_open_price_for_stocks(stocks)
            self.uow.stock_repo.bulk_update(stocks)
            self.uow.commit()
