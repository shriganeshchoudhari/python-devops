from release_sentinel.checks.system import check_process
from release_sentinel.checks.result import OK, CRIT

def test_process_check_ok_for_running_process():
    # Python test runner itself guarantees a python process exists
    res = check_process("python")
    assert res.status in (OK,)

def test_process_check_crit_for_fake_process():
    res = check_process("definitely_not_a_real_process_123")
    assert res.status == CRIT
