from typing import List

from domain.stock import Stock


class StockRepositoryBase:

    def save(self, stock: Stock):
        pass

    def bulk_update(self, stocks: List[Stock]):
        pass

    def get_list_by_symbols(self, symbols: List[str]) -> List[Stock]:
        pass

    def get_by_symbol(self, symbol: str) -> Stock:
        pass
