"""Unix epoch timestamp validator in milliseconds."""

import time
from typing import Annotated

from pydantic import BeforeValidator


def validate_epoch_ms(value: int) -> int:
    """Validate a Unix epoch timestamp in milliseconds.

    Args:
        value: The integer to validate as a Unix epoch timestamp in milliseconds.

    Returns:
        int: The validated epoch timestamp.

    Raises:
        ValueError: If the timestamp is in the future or negative.
    """
    current_ms = int(time.time() * 1000)

    if value < 0:
        raise ValueError("Epoch timestamp cannot be negative: %", value)

    if value > current_ms:
        raise ValueError("Epoch timestamp cannot be in the future: %s > %s", value, current_ms)

    return value


EpochMs = Annotated[int, BeforeValidator(validate_epoch_ms)]
