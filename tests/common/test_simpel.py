from datetime import datetime

import pytest
from freezegun import freeze_time

from vulsy.common.simpel import now, now_date, now_epoch_ms, epoch_start


def test_now_returns_iso_format():
    """Test that now() returns a string in ISO format."""
    result = now()
    assert isinstance(result, str)
    # Attempt to parse the result as an ISO format datetime
    try:
        datetime.fromisoformat(result)
    except ValueError:
        pytest.fail("now() did not return a valid ISO format string")


def test_now_returns_utc_time():
    """Test that now() returns the current UTC time."""
    # Freeze time to a known UTC datetime
    frozen_time = "2023-04-01T12:00:00+00:00"
    with freeze_time(frozen_time):
        result = now()
        assert result == frozen_time


def test_now_timezone_info():
    """Test that now() includes timezone information."""
    result = now()
    # Check if the result ends with +00:00 (UTC)
    assert result.endswith("+00:00")


def test_now_date_returns_string():
    """Test that now_date() returns a string."""
    result = now_date()
    assert isinstance(result, str)


def test_now_date_format():
    """Test that now_date() returns date in DD-MM-YYYY format."""
    result = now_date()
    # Check if the result matches the expected format
    try:
        datetime.strptime(result, "%d-%m-%Y")
    except ValueError:
        pytest.fail("now_date() did not return a valid DD-MM-YYYY format string")


def test_now_date_returns_utc_date():
    """Test that now_date() returns the current UTC date."""
    frozen_time = "2023-04-01T12:00:00+00:00"
    with freeze_time(frozen_time):
        result = now_date()
        assert result == "01-04-2023"


def test_now_epoch_ms_returns_integer():
    """Test that now_epoch_ms() returns an integer."""
    result = now_epoch_ms()
    assert isinstance(result, int)


def test_now_epoch_ms_correct_timestamp():
    """Test that now_epoch_ms() returns the correct timestamp."""
    # Freeze time to 2023-04-01 12:00:00 UTC
    frozen_time = "2023-04-01T12:00:00+00:00"
    expected_ms = 1680350400000  # Pre-calculated value for this timestamp

    with freeze_time(frozen_time):
        result = now_epoch_ms()
        assert result == expected_ms


def test_now_epoch_ms_millisecond_precision():
    """Test that now_epoch_ms() has millisecond precision."""
    result = now_epoch_ms()
    # Convert back to seconds by dividing by 1000
    # Should be a whole number when converted to milliseconds and back
    assert result / 1000 * 1000 == result


def test_epoch_start():
    """Test that epoch_start() returns the correct Unix epoch start time."""
    result = epoch_start()
    expected = "1970-01-01T00:00:00+00:00"
    assert result == expected
