from fastapi import Depends

from domain.stock import Stock
from infrastructure.gateways.alpha_vantage_gateway import AlphaVantageGateway
from infrastructure.repositories.stock import StockRepository


class GetStockService:

    def __init__(
            self,
            alpha_vantage_gateway: AlphaVantageGateway = Depends(AlphaVantageGateway),
            stock_repository: StockRepository = Depends(StockRepository)
    ):
        self.gateway = alpha_vantage_gateway
        self.repository = stock_repository

    async def get_stock_data(self, symbol: str) -> Stock:
        stock = self.repository.get_by_symbol(symbol)

        if not stock:
            stock = await self.gateway.get_stock_for_symbol(symbol)
            self.repository.save(stock)

        return stock
