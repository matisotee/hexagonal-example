import time
from typing import Any, Tuple, Union

import aiohttp
from aiohttp import ClientTimeout, ContentTypeError

from domain.exceptions import ServiceCallException
from infrastructure.config import LOGGER


class BaseGateway:  # pragma: no cover
    """
    Base Gateway class to be extended by all other API gateways
    """

    @staticmethod
    async def _make_request(method, headers, url, **kwargs: Any) -> Tuple[int, Union[dict, str]]:
        """
        Wrapper to make http request.
        """
        start_time = time.time()
        LOGGER.debug("Sending request", extra={"method": method, "url": url, "params": kwargs})
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=60)) as session:
            async with session.request(method=method, headers=headers, url=url, ssl=False, **kwargs) as resp:
                LOGGER.debug(
                    'Received response',
                    extra={
                        'url': url,
                        'status code': resp.status,
                        'durationMs': int((time.time() - start_time) * 1000)
                    }
                )
                try:
                    if resp.status != 200:
                        raise ServiceCallException()
                    return resp.status, await resp.json()
                except ContentTypeError:
                    return resp.status, await resp.text()

    @staticmethod
    async def get(url, headers=None, **kwargs: Any) -> Tuple[int, dict]:
        return await BaseGateway._make_request(method='GET', headers=headers, url=url, **kwargs)

    @staticmethod
    async def post(url, headers=None, **kwargs: Any) -> Tuple[int, dict]:
        return await BaseGateway._make_request(method='POST', headers=headers, url=url, **kwargs)

    @staticmethod
    async def put(url, headers=None, **kwargs: Any) -> Tuple[int, dict]:
        return await BaseGateway._make_request(method='PUT', headers=headers, url=url, **kwargs)

    @staticmethod
    async def delete(url, headers=None, **kwargs: Any) -> Tuple[int, dict]:
        return await BaseGateway._make_request(method='DELETE', headers=headers, url=url, **kwargs)