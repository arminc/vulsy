"""Valid CVE string."""

import re
from typing import Annotated

from pydantic import BeforeValidator


def validate_cve(value: str) -> str:
    """Validate a CVE string.

    Args:
        value: The string to validate as a CVE.

    Returns:
        str: The validated CVE string.

    Raises:
        ValueError: If the input is not a valid CVE format.
    """
    cve_pattern = r"^CVE-\d{4}-\d{4,7}$"
    if not re.match(cve_pattern, value):
        raise ValueError("Invalid CVE format: %s", value)
    return value


Cve = Annotated[str, BeforeValidator(validate_cve)]
