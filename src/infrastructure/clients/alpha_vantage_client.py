from typing import Any, Dict, Optional
from src.domain.clients.alpha_vantage_client import AlphaVantageClient
from src.domain.exceptions import StockNotFound
from src.domain.models.stock import Stock
from src.config import ALPHA_URL, ALPHA_API_KEY
from src.infrastructure.clients.http_client import JsonHttpClient


class AlphaVantageHttpClient(AlphaVantageClient):
    _SERVICE_NAME = "AlphaVantage"
    _HOST = ALPHA_URL
    _API_KEY = ALPHA_API_KEY
    _GET_STOCK_URL: str = "/query"

    def __init__(self, incoming_headers: Optional[Dict[str, Any]] = None):
        self.client = JsonHttpClient(service_name=self._SERVICE_NAME, host=self._HOST)
        self.headers = {"Content-Type": "application/json"}

        if incoming_headers:
            keys_to_copy = {
                "my-custom-header",
            }
            for key, value in incoming_headers.items():
                lower_key = key.lower()
                if lower_key in keys_to_copy:
                    self.headers[lower_key] = value

    async def get_stock_for_symbol(self, symbol: str) -> Stock:
        params = dict(
            function='TIME_SERIES_DAILY',
            symbol=symbol,
            outputsize='compact',
            apikey=self._API_KEY,
        )
        
        json_response = await self.client.make_request(
            url=self._GET_STOCK_URL,
            method="get",
            headers=self.headers,
            timeout=10,
            params=params,
        )
        if 'Error Message' in json_response:
            raise StockNotFound()
        return Stock.create_from_alpha_vantage_data(json_response)
