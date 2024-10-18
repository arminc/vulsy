"""Tests for Unix epoch timestamp validator."""

import time
from unittest.mock import patch

import pytest

from vulsy.common.types.epoch import validate_epoch_ms


def test_valid_epoch():
    """Test validation of a valid epoch timestamp."""
    current_ms = int(time.time() * 1000)
    past_ms = current_ms - 1000  # 1 second ago

    assert validate_epoch_ms(past_ms) == past_ms


def test_negative_epoch():
    """Test validation fails for negative epoch."""
    with pytest.raises(ValueError, match="Epoch timestamp cannot be negative"):
        validate_epoch_ms(-1)


def test_future_epoch():
    """Test validation fails for future epoch."""
    with patch("time.time") as mock_time:
        mock_time.return_value = 1000  # 1000 seconds since epoch
        current_ms = 1000 * 1000  # convert to milliseconds
        future_ms = current_ms + 1000  # 1 second in future

        with pytest.raises(ValueError, match="Epoch timestamp cannot be in the future"):
            validate_epoch_ms(future_ms)


def test_current_epoch():
    """Test validation of current epoch timestamp."""
    current_ms = int(time.time() * 1000)
    assert validate_epoch_ms(current_ms) == current_ms
