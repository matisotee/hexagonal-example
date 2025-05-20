from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.domain.exceptions import BaseApplicationException


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except BaseApplicationException as exception:
            return JSONResponse(
                content={"title": type(exception).__name__},
                status_code=400
            )
