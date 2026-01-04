# tests/test_core.py
import pytest
from mytool.core import calculate_disk_percentage

@pytest.mark.parametrize("used,total,expected", [
    (50, 100, 50.0),
    (0, 100, 0.0),
    (100, 100, 100.0),
])
def test_disk_percentage_normal(used, total, expected):
    assert calculate_disk_percentage(used, total) == expected

def test_disk_percentage_zero_total():
    with pytest.raises(ValueError):
        calculate_disk_percentage(10, 0)