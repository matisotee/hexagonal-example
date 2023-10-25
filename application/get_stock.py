from importlib import import_module

from fastapi import Depends

from domain.gateways.alpha_vantage_gateway import AlphaVantageGatewayBase
from domain.repositories.stock_repository import StockRepositoryBase
from domain.stock import Stock


class GetStockService:

    def __init__(
            self,
            alpha_vantage_gateway: AlphaVantageGatewayBase = Depends(getattr(import_module('infrastructure.gateways.alpha_vantage_gateway'), 'AlphaVantageGateway')),
            stock_repository: StockRepositoryBase = Depends(getattr(import_module('infrastructure.repositories.stock'), 'StockRepository'))
    ):
        self.gateway = alpha_vantage_gateway
        self.repository = stock_repository

    async def get_stock_data(self, symbol: str) -> Stock:
        stock = self.repository.get_by_symbol(symbol)

        if not stock:
            stock = await self.gateway.get_stock_for_symbol(symbol)
            self.repository.save(stock)

        return stock
