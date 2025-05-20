from fastapi import FastAPI

from src.infrastructure.controllers import get_stock, bulk_reset_stock_open_price
from src.infrastructure.controllers.middlewares import ExceptionMiddleware
from src.infrastructure.dependency_injection import Container


container = Container()

app = FastAPI()
app.container = container
app.include_router(get_stock.router)
app.include_router(bulk_reset_stock_open_price.router)
app.add_middleware(ExceptionMiddleware)
