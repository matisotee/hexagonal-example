from typing import List

from domain.stock import Stock


class StockOpenPriceResetter:

    @classmethod
    def reset_open_price_for_stocks(cls, stocks: List[Stock]):
        for stock in stocks:
            stock.reset_open_price()
