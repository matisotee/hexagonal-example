from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.domain.unit_of_work import SyncUnitOfWork
from src.infrastructure.persistence.repositories.sql_alchemy_stock_repository import SQLAlchemySyncStockRepository


# This is not completely working, use the Sync UOW

# class AsyncSqlAlchemyUnitOfWork(AsyncUnitOfWork):
#     DB_POOL_SIZE = 10

#     def __init__(self, db_connection_url: str):
#         self.engine = create_async_engine(db_connection_url, pool_size=self.DB_POOL_SIZE)
#         self.session_factory = async_sessionmaker(self.engine, expire_on_commit=True)
#         self.session = None

#     async def commit(self):
#         await self.session.commit()

#     async def close_connection(self):
#         await self.engine.dispose()

#     def _initialize_session(self):
#         self.session = self.session_factory()

#     def _initialize_repositories(self):
#         self.stock_repo = SQLAlchemyAsyncStockRepository(self.session)
#         pass

#     async def _rollback(self):
#         await self.session.rollback()

#     async def _close_session(self):
#         await self.session.close()
#         self.session = None


class SyncSqlAlchemyUnitOfWork(SyncUnitOfWork):
    DB_POOL_SIZE = 10

    def __init__(self, db_connection_url: str):
        self.engine = create_engine(db_connection_url, pool_size=self.DB_POOL_SIZE)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=True)
        self.session = None

    def commit(self):
        self.session.commit()

    def close_connection(self):
        self.engine.dispose()

    def _initialize_session(self):
        self.session = self.session_factory()

    def _initialize_repositories(self):
        self.stock_repo = SQLAlchemySyncStockRepository(self.session)

    def _rollback(self):
        self.session.rollback()

    def _close_session(self):
        self.session.close()
        self.session = None
