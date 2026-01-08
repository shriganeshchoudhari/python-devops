from release_sentinel.core import run_checks

def test_run_checks_returns_int():
    code = run_checks("dev", "v0.0.1")
    assert isinstance(code, int)
