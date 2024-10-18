import pytest
from pydantic import BaseModel, ValidationError

from vulsy.common.types.cve import Cve, validate_cve


class TempModel(BaseModel):
    cve: Cve


def test_validate_cve_valid():
    """Test that valid CVE strings are accepted."""
    valid_cves = [
        "CVE-2021-1234",
        "CVE-2023-12345",
        "CVE-2024-1234567",
    ]
    for cve in valid_cves:
        assert validate_cve(cve) == cve


def test_validate_cve_invalid():
    """Test that invalid CVE strings raise ValueError."""
    invalid_cves = [
        "CVE-202-1234",  # Year too short
        "CVE-20211-1234",  # Year too long
        "CVE-2021-123",  # ID too short
        "CVE-2021-12345678",  # ID too long
        "cve-2021-1234",  # Lowercase prefix
        "CVE-2021-abcd",  # Non-numeric ID
        "CVE2021-1234",  # Missing hyphen
        "CVE-2021-1234-extra",  # Extra content
        "NOT-A-CVE",
    ]
    for cve in invalid_cves:
        with pytest.raises(ValueError, match=f"('Invalid CVE format: %s', '{cve}')"):
            validate_cve(cve)


def test_cve_type_valid():
    valid_cve = "CVE-2023-12345"
    model = TempModel(cve=valid_cve)
    assert model.cve == valid_cve


def test_cve_type_invalid():
    invalid_cve = "NOT-A-CVE"
    with pytest.raises(ValidationError):
        TempModel(cve=invalid_cve)


def test_cve_type_non_string():
    non_string_inputs = [123, True, None, ["CVE-2023-1234"]]
    for input_value in non_string_inputs:
        with pytest.raises(TypeError):
            TempModel(cve=input_value)
