import asyncio
from unittest.mock import MagicMock

from application.get_stock import GetStockService
from domain.stock import Stock
import pytest


@pytest.mark.asyncio
async def test_get_stock_with_stored_stock():
    expected_result = Stock(
        symbol='AAPL', open_price='1', higher_price='1', lower_price='1', variation='1'
    )
    mock_repo = MagicMock()
    mock_repo.get_by_symbol.return_value = expected_result
    mock_gateway = MagicMock()
    service = GetStockService(mock_gateway, mock_repo)

    result = await service.get_stock_data('AAPL')

    assert expected_result == result
    mock_repo.get_by_symbol.assert_called_once_with('AAPL')
    mock_gateway.get_stock_for_symbol.assert_not_called()


@pytest.mark.asyncio
async def test_get_stock_with_not_stored_stock():
    expected_result = Stock(
        symbol='AAPL', open_price='1', higher_price='1', lower_price='1', variation='1'
    )
    expected_result_async = asyncio.Future()
    expected_result_async.set_result(expected_result)
    mock_repo = MagicMock()
    mock_repo.get_by_symbol.return_value = None
    mock_gateway = MagicMock()
    mock_gateway.get_stock_for_symbol.return_value = expected_result_async
    service = GetStockService(mock_gateway, mock_repo)

    result = await service.get_stock_data('AAPL')

    assert expected_result == result
    mock_repo.get_by_symbol.assert_called_once_with('AAPL')
    mock_gateway.get_stock_for_symbol.assert_called_once_with('AAPL')

