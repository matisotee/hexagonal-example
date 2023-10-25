from fastapi import FastAPI

from infrastructure.controllers import get_stock, bulk_reset_stock_open_price
from infrastructure.controllers.middlewares import ExceptionMiddleware

app = FastAPI()
app.include_router(get_stock.router)
app.include_router(bulk_reset_stock_open_price.router)
app.add_middleware(ExceptionMiddleware)
