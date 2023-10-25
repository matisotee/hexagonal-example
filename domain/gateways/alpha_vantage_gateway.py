from domain.stock import Stock


class AlphaVantageGatewayBase:

    @classmethod
    async def get_stock_for_symbol(cls, symbol: str) -> Stock:
        pass
