"""HTTP client."""

from enum import StrEnum
from typing import Any

import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry


class HTTPRequestError(Exception):
    """Custom exception for HTTP request errors."""


class HTTPRequestConfig(BaseModel):
    """Configuration for HTTP requests."""

    timeout: float = 60.0
    retries: int = 3
    backoff_factor: float = 0.3


class HTTPMethod(StrEnum):
    """HTTP methods that are supported."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


def http_request(
    url: str,
    method: HTTPMethod = HTTPMethod.GET,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    config: HTTPRequestConfig | None = None,
    data: Any | None = None,  # noqa: ANN401
) -> requests.Response:
    """Perform an HTTP request with retries and error handling.

    Args:
        url: The URL to request.
        method: HTTP method to use (e.g., 'GET', 'POST').
        params: Optional query parameters to include in the request.
        headers: Optional headers to include in the request.
        config: Configuration object for request settings.
        data: (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body

    Returns:
        The HTTP response object.

    Raises:
        HTTPRequestError: If the request fails or the response status is not 200.
    """
    if config is None:
        config = HTTPRequestConfig()
    headers = headers or {}
    session = requests.Session()
    retry_strategy = Retry(
        total=config.retries,
        backoff_factor=config.backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.request(
            method,
            url,
            headers=headers,
            params=params,
            timeout=config.timeout,
            data=data,
        )
        response.raise_for_status()
        return response
    except RequestException as e:
        raise HTTPRequestError("Request failed") from e


def get_json(
    url: str,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    config: HTTPRequestConfig | None = None,
) -> dict:
    """Get JSON response from a URL.

    Args:
        url: The URL to request.
        params: Optional query parameters to include in the request.
        headers: Optional headers to include in the request.
        config: Configuration object for request settings.

    Returns:
        The JSON response as a dictionary.

    Raises:
        HTTPRequestError: If the request fails or the response is not valid JSON.
    """
    if config is None:
        config = HTTPRequestConfig()
    response = http_request(url, params=params, headers=headers, config=config)
    try:
        return response.json()
    except ValueError as e:
        raise HTTPRequestError("Failed to parse JSON response") from e


def get_text(
    url: str,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    config: HTTPRequestConfig | None = None,
) -> str:
    """Get text response from a URL.

    Args:
        url: The URL to request.
        params: Optional query parameters to include in the request.
        headers: Optional headers to include in the request.
        config: Configuration object for request settings.

    Returns:
        The text response.

    Raises:
        HTTPRequestError: If the request fails.
    """
    if config is None:
        config = HTTPRequestConfig()
    response = http_request(url, params=params, headers=headers, config=config)
    return response.text
