from abc import abstractmethod
from typing import List

from src.domain.models.stock import Stock


class SyncStockRepository:

    @abstractmethod
    def save(self, stock: Stock):
        pass

    @abstractmethod
    def bulk_update(self, stocks: List[Stock]):
        pass

    @abstractmethod
    def get_list_by_symbols(self, symbols: List[str]) -> List[Stock]:
        pass

    @abstractmethod
    def get_by_symbol(self, symbol: str) -> Stock:
        pass


# Async repository, this is not completely working, prefer sync repos

# class AsyncStockRepository:
    
#     @abstractmethod
#     async def save(self, stock: Stock):
#         pass

#     @abstractmethod
#     async def bulk_update(self, stocks: List[Stock]):
#         pass

#     @abstractmethod
#     async def get_list_by_symbols(self, symbols: List[str]) -> List[Stock]:
#         pass

#     @abstractmethod
#     async def get_by_symbol(self, symbol: str) -> Stock:
#         pass 
