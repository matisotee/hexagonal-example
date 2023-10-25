from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
import uuid

from domain.stock import Stock
from infrastructure.config import DB_URL
from infrastructure.repositories.stock import StockRepository


def get_test_session():
    engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return test_session()


def test_stock_is_correctly_saved_and_retrieved():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    symbol = str(uuid.uuid4())
    stock = Stock(
        symbol=symbol, open_price='1', higher_price='1', lower_price='1', variation='1'
    )
    session = get_test_session()
    repo = StockRepository(session)

    repo.save(stock)
    result = repo.get_by_symbol(symbol)

    assert result == stock
