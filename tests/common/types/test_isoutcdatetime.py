import pytest
from pydantic import BaseModel, ValidationError

from vulsy.common.types.isoutcdatetime import IsoUtcDateTime, validate_iso_utc_datetime


class TempModel(BaseModel):
    datetime_field: IsoUtcDateTime


def test_valid_iso_utc_datetime():
    """Test valid ISO UTC datetime strings."""
    valid_datetimes = [
        "2023-04-01T12:00:00Z",
        "2023-04-01T12:00:00+00:00",
        "2023-04-01T12:00:00-00:00",
        "2023-04-01T12:00:00.123456+00:00",
        "2023-04-01T12:00:00+05:30",
        "2023-04-01T12:00:00-08:00",
    ]

    for dt in valid_datetimes:
        model = TempModel(datetime_field=dt)
        assert model.datetime_field.endswith("+00:00")


def test_invalid_iso_datetime():
    """Test invalid ISO UTC datetime strings."""
    invalid_datetimes = [
        "2023-04-01 12:00:00",  # Missing 'T' separator
        "2023-04-01T12:00:00",  # Missing timezone
        "2023-04-01T25:00:00Z",  # Invalid hour
        "2023-04-01T12:60:00Z",  # Invalid minute
        "2023-04-01T12:00:60Z",  # Invalid second
    ]

    for dt in invalid_datetimes:
        with pytest.raises(ValidationError):
            TempModel(datetime_field=dt)


def test_timezone_conversion():
    """Test timezone conversion to UTC."""
    test_cases = [
        ("2023-04-01T12:00:00+05:30", "2023-04-01T06:30:00+00:00"),
        ("2023-04-01T12:00:00-08:00", "2023-04-01T20:00:00+00:00"),
        ("2023-04-01T00:00:00+01:00", "2023-03-31T23:00:00+00:00"),
    ]

    for input_dt, expected_dt in test_cases:
        model = TempModel(datetime_field=input_dt)
        assert model.datetime_field == expected_dt


def test_microsecond_precision():
    """Test microsecond precision is preserved."""
    input_dt = "2023-04-01T12:00:00.123456+00:00"
    model = TempModel(datetime_field=input_dt)
    assert model.datetime_field == input_dt


def test_validate_iso_utc_datetime_function():
    """Test the validate_iso_utc_datetime function directly."""
    valid_dt = "2023-04-01T12:00:00+05:30"
    assert validate_iso_utc_datetime(valid_dt) == "2023-04-01T06:30:00+00:00"

    invalid_dt = "2023-04-01 12:00:00"
    with pytest.raises(ValueError, match="Invalid ISO datetime format. Must include timezone."):
        validate_iso_utc_datetime(invalid_dt)


def test_edge_cases():
    """Test edge cases for ISO UTC datetime."""
    edge_cases = [
        "9999-12-31T23:59:59.999999+00:00",  # Maximum valid date
        "0001-01-01T00:00:00+00:00",  # Minimum valid date
    ]

    for dt in edge_cases:
        model = TempModel(datetime_field=dt)
        assert model.datetime_field == dt

    # We ignore microseconds
    micro = "2023-04-01T00:00:00.000000+00:00"
    assert validate_iso_utc_datetime(micro) == "2023-04-01T00:00:00+00:00"
