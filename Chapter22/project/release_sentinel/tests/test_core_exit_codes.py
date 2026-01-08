import pytest
from release_sentinel.core import run_checks

def test_core_blocks_on_missing_config(monkeypatch):
    monkeypatch.delenv("RS_REQUIRED_PROCESS", raising=False)
    monkeypatch.delenv("RS_API_URL", raising=False)
    monkeypatch.delenv("RS_DEPLOY_TOKEN", raising=False)

    code = run_checks(env="dev", version="v0.1.0")
    assert code == 1
