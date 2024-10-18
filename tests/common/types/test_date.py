"""Tests for date string validator."""

import pytest

from vulsy.common.types.date import validate_date_string


def test_valid_date():
    """Test validation of a valid date string."""
    assert validate_date_string("1-1-2024") == "1-1-2024"
    assert validate_date_string("01-01-2024") == "01-01-2024"
    assert validate_date_string("31-12-2023") == "31-12-2023"
    assert validate_date_string("29-02-2024") == "29-02-2024"  # Leap year


def test_invalid_format():
    """Test validation fails with incorrect format."""
    invalid_formats = [
        "2024-01-01",  # YYYY-MM-DD
        "01/01/2024",  # Wrong separator
        "01-01-24",  # Two-digit year
    ]

    for date_str in invalid_formats:
        with pytest.raises(ValueError, match="Date must be in DD-MM-YYYY format"):
            validate_date_string(date_str)


def test_invalid_dates():
    """Test validation fails with invalid dates."""
    invalid_dates = [
        "32-01-2024",  # Invalid day
        "01-13-2024",  # Invalid month
        "29-02-2023",  # Not a leap year
        "31-04-2024",  # April has 30 days
    ]

    for date_str in invalid_dates:
        with pytest.raises(ValueError):
            validate_date_string(date_str)


def test_invalid_types():
    """Test validation fails with non-string inputs."""
    invalid_inputs = [
        None,
        123,
        True,
        ["01-01-2024"],
    ]

    for invalid_input in invalid_inputs:
        with pytest.raises((ValueError, TypeError)):
            validate_date_string(invalid_input)  # type: ignore
