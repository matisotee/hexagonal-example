"""Containers module."""

from dependency_injector import containers, providers

from src.application.bulk_reset_stock_open_price import BulkResetStockOpenPriceService
from src.application.get_stock import GetStockService
from src.config import DB_URL
from src.infrastructure.clients.alpha_vantage_client import AlphaVantageHttpClient
from src.infrastructure.persistence.sql_alchemy_unit_of_work import SyncSqlAlchemyUnitOfWork


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.infrastructure.controllers.get_stock",
            "src.infrastructure.controllers.bulk_reset_stock_open_price",
        ]
    )

    sync_uow = providers.Singleton(SyncSqlAlchemyUnitOfWork, db_connection_url=DB_URL)

    alpha_vantage_client = providers.Factory(AlphaVantageHttpClient)

    get_stock_service = providers.Factory(
        GetStockService,
        alpha_vantage_client=alpha_vantage_client,
        uow=sync_uow,
    )

    bulk_reset_stock_open_price_service = providers.Factory(
        BulkResetStockOpenPriceService,
        uow=sync_uow,
    )