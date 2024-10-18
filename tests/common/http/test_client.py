import pytest
import requests_mock

from vulsy.common.http.client import HTTPRequestConfig, HTTPRequestError, get_json, get_text, http_request


def test_http_request_success():
    with requests_mock.Mocker() as m:
        m.get("http://test.com", text="success")
        response = http_request("http://test.com")
        assert response.text == "success"


def test_http_request_failure():
    with requests_mock.Mocker() as m:
        m.get("http://test.com", status_code=500)
        with pytest.raises(HTTPRequestError):
            http_request("http://test.com")


def test_get_json_success():
    with requests_mock.Mocker() as m:
        m.get("http://test.com", json={"key": "value"})
        response = get_json("http://test.com")
        assert response == {"key": "value"}


def test_get_json_failure():
    with requests_mock.Mocker() as m:
        m.get("http://test.com", text="not a json")
        with pytest.raises(HTTPRequestError):
            get_json("http://test.com")


def test_get_text_success():
    with requests_mock.Mocker() as m:
        m.get("http://test.com", text="some text")
        response = get_text("http://test.com")
        assert response == "some text"


def test_http_request_with_custom_config():
    config = HTTPRequestConfig(timeout=10.0, retries=5, backoff_factor=0.1)
    with requests_mock.Mocker() as m:
        m.get("http://test.com", text="success")
        response = http_request("http://test.com", config=config)
        assert response.text == "success"
