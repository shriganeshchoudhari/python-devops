import pytest
from release_sentinel.checks.env import ensure_env_allowed

def test_valid_envs():
    for env in ("dev", "stage", "prod"):
        ensure_env_allowed(env)

def test_invalid_env_blocks():
    with pytest.raises(RuntimeError):
        ensure_env_allowed("production")
