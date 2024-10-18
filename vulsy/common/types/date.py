"""Date string validator in DD-MM-YYYY format."""

from datetime import datetime
from typing import Annotated

from pydantic import BeforeValidator


def validate_date_string(value: str) -> str:
    """Validate a date string in DD-MM-YYYY format.

    Args:
        value: The string to validate as a date in DD-MM-YYYY format.

    Returns:
        str: The validated date string.

    Raises:
        ValueError: If the string is not in the correct format or not a valid date.
    """
    try:
        datetime.strptime(value, "%d-%m-%Y")  # noqa: DTZ007 TZ is not relevant here
    except ValueError as e:
        raise ValueError("Date must be in DD-MM-YYYY format, got: %s", value) from e

    return value


DateString = Annotated[str, BeforeValidator(validate_date_string)]
