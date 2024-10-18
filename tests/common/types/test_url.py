import pytest
from pydantic import BaseModel, ValidationError

from vulsy.common.types.url import HttpUrl, validate_url


class TempModel(BaseModel):
    url: HttpUrl


def test_valid_http_url():
    valid_url = "http://example.com/"
    assert validate_url(valid_url) == valid_url


def test_valid_https_url():
    valid_url = "https://example.com/"
    assert validate_url(valid_url) == valid_url


def test_valid_url_with_path():
    valid_url = "https://example.com/path/to/resource"
    assert validate_url(valid_url) == valid_url


def test_valid_url_with_query_params():
    valid_url = "https://example.com/search?q=test&page=1"
    assert validate_url(valid_url) == valid_url


def test_invalid_url_scheme():
    valid_url = "ftp://example.com/"
    assert validate_url(valid_url) == valid_url


def test_invalid_url_format():
    with pytest.raises(ValidationError):
        TempModel(url="not_a_url")


def test_url_without_scheme():
    with pytest.raises(ValidationError):
        TempModel(url="example.com")


def test_url_with_ip_address():
    valid_url = "http://192.168.1.1/"
    assert validate_url(valid_url) == valid_url


def test_url_with_port():
    valid_url = "http://example.com:8080/"
    assert validate_url(valid_url) == valid_url


def test_url_with_username_password():
    valid_url = "http://user:pass@example.com/"
    assert validate_url(valid_url) == valid_url
