"""ISO UTC datetime string."""

import re
from datetime import UTC, datetime
from typing import Annotated

from pydantic import BeforeValidator


def validate_iso_utc_datetime(value: str) -> str:
    """Validate and convert ISO datetime string to UTC.

    Args:
        value: ISO datetime string with timezone information.

    Returns:
        UTC datetime string in ISO format with +00:00 timezone representation.

    Raises:
        ValueError: If the input is not a valid ISO datetime string with timezone.
    """
    iso_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(([+-]\d{2}:\d{2})|Z)$"
    if not re.match(iso_regex, value):
        raise ValueError("Invalid ISO datetime format. Must include timezone.")

    dt = datetime.fromisoformat(value)
    utc_dt = dt.astimezone(UTC)
    return utc_dt.isoformat()


IsoUtcDateTime = Annotated[str, BeforeValidator(validate_iso_utc_datetime)]
