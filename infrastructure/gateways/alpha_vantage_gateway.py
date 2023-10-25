from domain.exceptions import ServiceCallException, StockNotFound
from domain.gateways.alpha_vantage_gateway import AlphaVantageGatewayBase
from domain.stock import Stock
from infrastructure.config import ALPHA_URL, ALPHA_API_KEY
from infrastructure.gateways.base import BaseGateway


class AlphaVantageGateway(AlphaVantageGatewayBase, BaseGateway):
    _BASE_URL = f'{ALPHA_URL}query'
    _API_KEY = ALPHA_API_KEY

    @classmethod
    async def get_stock_for_symbol(cls, symbol: str) -> Stock:
        params = dict(
            function='TIME_SERIES_DAILY',
            symbol=symbol,
            outputsize='compact',
            apikey=cls._API_KEY,
        )
        # TODO: manage error, response code and do proper logging
        try:
            status_code, json_response = await cls.get(cls._BASE_URL, params=params)
            if 'Error Message' in json_response:
                raise StockNotFound()
        except ServiceCallException:
            raise StockNotFound()

        return Stock.create_from_alpha_vantage_data(json_response)
