"""Valid URL string."""

from typing import Annotated

from pydantic import BeforeValidator
from pydantic import HttpUrl as PydanticHttpUrl


def validate_url(value: str) -> str:
    """Validate and convert a URL string to a standardized format.

    Args:
        value: The URL string to validate.

    Returns:
        A validated and standardized URL string.

    Raises:
        ValueError: If the URL is invalid.
    """
    return str(PydanticHttpUrl(value))


HttpUrl = Annotated[str, BeforeValidator(validate_url)]
