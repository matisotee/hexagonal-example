from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from src.application.bulk_reset_stock_open_price import BulkResetStockOpenPriceService
from src.infrastructure.dependency_injection import Container

router = APIRouter()


@router.post("/stocks/reset")
@inject
def get_stock_market(
        symbols: List[str],
        service: BulkResetStockOpenPriceService = Depends(Provide[Container.bulk_reset_stock_open_price_service])
):
    service.bulk_reset_stock_open_price(symbols)
    return JSONResponse(content={"message": "success"})
