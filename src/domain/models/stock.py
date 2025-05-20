from typing import Dict

from pydantic import BaseModel


class Stock(BaseModel):
    symbol: str
    open_price: str
    higher_price: str
    lower_price: str
    variation: str

    class Config:
        from_attributes = True

    @classmethod
    def create_from_alpha_vantage_data(cls, json_response: Dict):
        symbol = json_response['Meta Data']['2. Symbol']
        unsorted_daily_data = json_response['Time Series (Daily)']
        daily_data = dict(sorted(unsorted_daily_data.items()))
        last_date = list(daily_data.keys())[-1]
        previous_date = list(daily_data.keys())[-2]

        open_price = daily_data[last_date]['1. open']
        higher_price = daily_data[last_date]['2. high']
        lower_price = daily_data[last_date]['3. low']
        close_price = float(daily_data[last_date]['4. close'])
        previous_close_price = float(daily_data[previous_date]['4. close'])
        variation = cls._get_variation(close_price, previous_close_price)
        return cls(
            symbol=symbol,
            open_price=open_price,
            higher_price=higher_price,
            lower_price=lower_price,
            variation=variation
        )

    def reset_open_price(self):
        self.open_price = '0'

    @classmethod
    def _get_variation(cls, current_value: float, previous_value: float) -> str:
        variation = ((current_value - previous_value) / previous_value) * 100
        rounded_variation = round(variation, 2)
        return f'{rounded_variation}%'
