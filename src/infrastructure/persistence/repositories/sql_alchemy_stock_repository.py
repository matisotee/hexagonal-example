from typing import List

from sqlalchemy import select, update
from sqlalchemy.orm import Session
# from sqlalchemy.ext.asyncio.session import AsyncSession

from src.domain.repositories.stock_repository import SyncStockRepository
from src.domain.models.stock import Stock
from src.infrastructure.persistence.sql_alchemy_schemas import StockOrmSchema


class SQLAlchemySyncStockRepository(SyncStockRepository):

    def __init__(self, session: Session):
        self.session = session

    def upsert(self, stock: Stock):
        self.session.merge(StockOrmSchema(**stock.model_dump()))

    def bulk_update(self, stocks: List[Stock]):
        updates = [stock.model_dump() for stock in stocks]

        self.session.execute(update(StockOrmSchema), updates)

    def get_list_by_symbols(self, symbols: List[str]) -> List[Stock]:
        stmt = select(StockOrmSchema).filter(
            StockOrmSchema.symbol.in_(symbols)
        )  # type: ignore
        result = self.session.execute(stmt)
        stock_schemas = result.scalars().all()

        if not stock_schemas:
            return []
        
        return [Stock.model_validate(stock_schema) for stock_schema in stock_schemas]

    def get_by_symbol(self, symbol: str) -> Stock:    
        stmt = select(StockOrmSchema).filter(StockOrmSchema.symbol == symbol)  # type: ignore
        result = self.session.execute(stmt)
        stock_schema = result.scalars().first()

        if not stock_schema:
            return None
        return Stock.model_validate(stock_schema)
    
    def bulk_add(self, stocks: List[Stock]) -> None:
        objects = [StockOrmSchema(**stock.model_dump()) for stock in stocks]
        self.session.add_all(objects)


# Async repository, this is not completely working, prefer sync repos

# class SQLAlchemyAsyncStockRepository(AsyncStockRepository):

#     def __init__(self, session: AsyncSession):
#         self.session = session

#     async def upsert(self, stock: Stock):
#         await self.session.merge(StockOrmSchema(**stock.model_dump()))

#     async def bulk_update(self, stocks: List[Stock]):
#         updates = [stock.model_dump() for stock in stocks]

#         await self.session.execute(update(StockOrmSchema), updates)

#     async def get_list_by_symbols(self, symbols: List[str]) -> List[Stock]:
#         stmt = select(StockOrmSchema).filter(
#             StockOrmSchema.symbol.in_(symbols)
#         )  # type: ignore
#         result = await self.session.execute(stmt)
#         stock_schemas = result.scalars().all()

#         if not stock_schemas:
#             return []
        
#         return [Stock.model_validate(stock_schema) for stock_schema in stock_schemas]

#     async def get_by_symbol(self, symbol: str) -> Stock:    
#         stmt = select(StockOrmSchema).filter(StockOrmSchema.symbol == symbol)  # type: ignore
#         result = await self.session.execute(stmt)
#         stock_schema = result.scalars().first()

#         if not stock_schema:
#             return None
#         return Stock.model_validate(stock_schema)
    
#     async def bulk_add(self, stocks: List[Stock]) -> None:
#         objects = [StockOrmSchema(**stock.model_dump()) for stock in stocks]
#         await self.session.add_all(objects) # TEST IT