import os
import pytest
from release_sentinel.checks.config import ensure_required_config

def test_missing_env_vars_block(monkeypatch):
    monkeypatch.delenv("RS_REQUIRED_PROCESS", raising=False)
    monkeypatch.delenv("RS_API_URL", raising=False)
    monkeypatch.delenv("RS_DEPLOY_TOKEN", raising=False)

    with pytest.raises(RuntimeError):
        ensure_required_config()

def test_required_env_vars_pass(monkeypatch):
    monkeypatch.setenv("RS_REQUIRED_PROCESS", "python")
    monkeypatch.setenv("RS_API_URL", "https://api.github.com")
    monkeypatch.setenv("RS_DEPLOY_TOKEN", "secret")

    cfg = ensure_required_config()
    assert cfg["process"] == "python"
    assert cfg["api_url"].startswith("https://")
