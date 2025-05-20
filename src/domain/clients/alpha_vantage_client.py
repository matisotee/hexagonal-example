from src.domain.models.stock import Stock


class AlphaVantageClient:

    async def get_stock_for_symbol(self, symbol: str) -> Stock:
        pass
