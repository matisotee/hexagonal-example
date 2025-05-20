from src.domain.clients.alpha_vantage_client import AlphaVantageClient
from src.domain.models.stock import Stock
from src.domain.unit_of_work import SyncUnitOfWork


class GetStockService:

    def __init__(
            self,
            alpha_vantage_client: AlphaVantageClient,
            uow: SyncUnitOfWork
    ):
        self.alpha_vantage_client = alpha_vantage_client
        self.uow = uow

    async def get_stock_data(self, symbol: str) -> Stock:
        with self.uow:
            stock = self.uow.stock_repo.get_by_symbol(symbol)

            if not stock:
                stock = await self.alpha_vantage_client.get_stock_for_symbol(symbol)
                self.uow.stock_repo.save(stock)
                self.uow.commit()

            return stock
