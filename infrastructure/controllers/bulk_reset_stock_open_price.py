from typing import List

from fastapi import APIRouter, Depends

from application.bulk_reset_stock_open_price import BulkResetStockOpenPriceService
from domain.stock import Stock

router = APIRouter()


@router.post("/stocks/reset")
def get_stock_market(
        symbols: List[str],
        service: BulkResetStockOpenPriceService = Depends(BulkResetStockOpenPriceService)
):
    service.bulk_reset_stock_open_price(symbols)
