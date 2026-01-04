import pytest
import requests
from deploy_guard.core.api_checks import get_with_retry

class DummyResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code

def test_api_success(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url, timeout: DummyResponse(200))
    assert get_with_retry("http://fake") == 0

def test_api_retry_then_success(monkeypatch):
    calls = {"count": 0}
    def fake_get(url, timeout):
        calls["count"] += 1
        if calls["count"] < 2:
            raise requests.exceptions.RequestException("Temporary error")
        return DummyResponse(200)
    monkeypatch.setattr(requests, "get", fake_get)
    assert get_with_retry("http://fake") == 0

def test_api_final_failure(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda url, timeout: (_ for _ in ()).throw(requests.exceptions.RequestException("Fail")))
    assert get_with_retry("http://fake") == 2