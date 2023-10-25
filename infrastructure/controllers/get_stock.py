from fastapi import APIRouter, Depends

from application.get_stock import GetStockService
from domain.stock import Stock

router = APIRouter()


@router.get("/stocks/{symbol}", response_model=Stock)
async def get_stock_market(symbol: str, stock_service: GetStockService = Depends(GetStockService)):
    return await stock_service.get_stock_data(symbol)
