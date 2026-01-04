import psutil
from deploy_guard.core.health_checks import check_disk, check_memory

def test_disk_ok(monkeypatch):
    monkeypatch.setattr(psutil, "disk_usage", lambda _: type("obj", (), {"percent": 50})())
    assert check_disk() == 0

def test_disk_warn(monkeypatch):
    monkeypatch.setattr(psutil, "disk_usage", lambda _: type("obj", (), {"percent": 80})())
    assert check_disk() == 0  # WARN still exit 0

def test_disk_critical(monkeypatch):
    monkeypatch.setattr(psutil, "disk_usage", lambda _: type("obj", (), {"percent": 90})())
    assert check_disk() == 2

def test_memory_ok(monkeypatch):
    monkeypatch.setattr(psutil, "virtual_memory", lambda: type("obj", (), {"percent": 50})())
    assert check_memory() == 0

def test_memory_warn(monkeypatch):
    monkeypatch.setattr(psutil, "virtual_memory", lambda: type("obj", (), {"percent": 75})())
    assert check_memory() == 0

def test_memory_critical(monkeypatch):
    monkeypatch.setattr(psutil, "virtual_memory", lambda: type("obj", (), {"percent": 90})())
    assert check_memory() == 2