import json
import logging

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import httpx

from httpx import AsyncClient


DEFAULT_CLIENT_TIMEOUT = 5


class HttpClient(ABC):

    def __init__(self, service_name: str, host: str):
        self.service_name = service_name
        self.host = host

    # pylint: disable=too-many-positional-arguments
    async def make_request(
        self,
        url: str,
        method: str = "get",
        headers: Optional[Dict] = None,
        timeout: Optional[int] = DEFAULT_CLIENT_TIMEOUT,
        payload: Optional[Any] = None,
        params: Optional[Any] = None,
    ) -> Any:

        full_url = f"{self.host}{url}"
        logging.info(
            "Starting call to service.",
            extra={
                "url": full_url,
                "service": self.service_name,
            },
        )
        if payload:
            payload = self._parse_payload(payload)

        async with AsyncClient() as client:
            match method:
                case "post":
                    response = await client.post(full_url, data=payload, headers=headers, params=params, timeout=timeout)
                case "put":
                    response = await client.put(full_url, data=payload, headers=headers, params=params, timeout=timeout)
                case "delete":
                    response = await client.delete(full_url, headers=headers, params=params, timeout=timeout)
                case _:
                    response = await client.get(full_url, headers=headers, params=params, timeout=timeout)

        response.raise_for_status()

        response_data = self._get_response_data(response)

        logging.info(
            "Finished call to service.",
            extra={
                "url": full_url,
                "status_code": response.status_code,
                "service": self.service_name,
            },
        )
        return response_data

    @staticmethod
    @abstractmethod
    def _get_response_data(response: httpx.Response) -> Any:  # pragma: no cover
        pass

    @staticmethod
    @abstractmethod
    def _parse_payload(payload: Any) -> Optional[str]:  # pragma: no cover
        pass


class JsonHttpClient(HttpClient):

    @staticmethod
    def _get_response_data(response: httpx.Response) -> Any:
        return response.json()

    @staticmethod
    def _parse_payload(payload: Any) -> Optional[str]:
        return json.dumps(payload)
