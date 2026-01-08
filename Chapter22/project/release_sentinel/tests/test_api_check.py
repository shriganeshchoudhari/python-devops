from release_sentinel.checks.api import check_api
from release_sentinel.checks.result import OK, CRIT

def test_api_ok():
    res = check_api("https://api.github.com", retries=1)
    assert res.status == OK

def test_api_critical_on_bad_url():
    res = check_api("http://127.0.0.1:9", retries=1)
    assert res.status == CRIT
