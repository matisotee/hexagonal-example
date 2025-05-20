from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from src.application.get_stock import GetStockService
from src.domain.models.stock import Stock
from src.infrastructure.dependency_injection import Container

router = APIRouter()


@router.get("/stocks/{symbol}", response_model=Stock)
@inject
async def get_stock_market(symbol: str, stock_service: GetStockService = Depends(Provide[Container.get_stock_service])):
    return await stock_service.get_stock_data(symbol)
