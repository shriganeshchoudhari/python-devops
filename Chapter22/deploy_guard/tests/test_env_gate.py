import os, pytest
from deploy_guard.core.env_gate import validate_env

def test_valid_env(monkeypatch):
    monkeypatch.setenv("ENV", "dev")
    monkeypatch.setenv("KUBECONFIG", "/fake/path")
    monkeypatch.setenv("SERVICE_URL", "http://localhost")
    monkeypatch.setenv("VERSION", "v1.0.0")
    assert validate_env() == 0

def test_invalid_env(monkeypatch):
    monkeypatch.setenv("ENV", "invalid")
    monkeypatch.setenv("KUBECONFIG", "/fake/path")
    monkeypatch.setenv("SERVICE_URL", "http://localhost")
    monkeypatch.setenv("VERSION", "v1.0.0")
    assert validate_env() == 2

def test_missing_secret(monkeypatch):
    monkeypatch.setenv("ENV", "dev")
    monkeypatch.delenv("KUBECONFIG", raising=False)
    monkeypatch.setenv("SERVICE_URL", "http://localhost")
    monkeypatch.setenv("VERSION", "v1.0.0")
    assert validate_env() == 2