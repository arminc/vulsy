"""Simple utlity functions."""

import time
from datetime import UTC, datetime


def now() -> str:
    """Get the current UTC time as an ISO 8601 formatted string.

    This function returns the current UTC time using the `datetime.now()`
    method with the UTC timezone. The result is then formatted as an
    ISO 8601 string using the `isoformat()` method.

    Returns:
        str: The current UTC time as an ISO 8601 formatted string.

    Example:
        >>> now()
        '2023-04-15T12:34:56.789012+00:00'
    """
    return datetime.now(UTC).isoformat()


def now_date() -> str:
    """Get the current UTC date as a DD-MM-YYYY formatted string.

    Returns:
        str: The current UTC date as a DD-MM-YYYY formatted string.

    Example:
        >>> now_date()
        '15-04-2023'
    """
    return datetime.now(UTC).strftime("%d-%m-%Y")


def now_epoch_ms() -> int:
    """Get the current UTC time as an epoch timestamp in milliseconds.

    Returns:
        int: The current UTC time as an epoch timestamp in milliseconds.

    Example:
        >>> now_epoch_ms()
        1715548800000
    """
    return int(time.time() * 1000)


def epoch_start() -> str:
    """Get the Unix epoch start time (1970-01-01T00:00:00+00:00) as an ISO 8601 formatted string.

    Returns:
        str: The Unix epoch start time as an ISO 8601 formatted string.

    Example:
        >>> epoch_start()
        '1970-01-01T00:00:00+00:00'
    """
    return datetime.fromtimestamp(0, UTC).isoformat()
