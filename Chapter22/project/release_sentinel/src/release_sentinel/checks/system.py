import shutil
import psutil
from release_sentinel.checks.result import CheckResult, OK, WARN, CRIT

DISK_WARN = 75
DISK_CRIT = 85
MEM_WARN = 70
MEM_CRIT = 85

def check_disk(path="/") -> CheckResult:
    total, used, _ = shutil.disk_usage(path)
    pct = (used / total) * 100

    if pct >= DISK_CRIT:
        return CheckResult(CRIT, f"Disk CRITICAL: {pct:.1f}%")
    if pct >= DISK_WARN:
        return CheckResult(WARN, f"Disk WARNING: {pct:.1f}%")
    return CheckResult(OK, f"Disk OK: {pct:.1f}%")

def check_memory() -> CheckResult:
    pct = psutil.virtual_memory().percent

    if pct >= MEM_CRIT:
        return CheckResult(CRIT, f"Memory CRITICAL: {pct:.1f}%")
    if pct >= MEM_WARN:
        return CheckResult(WARN, f"Memory WARNING: {pct:.1f}%")
    return CheckResult(OK, f"Memory OK: {pct:.1f}%")

def check_process(name: str) -> CheckResult:
    for p in psutil.process_iter(["name"]):
        if p.info["name"] and p.info["name"].lower().startswith(name.lower()):
            return CheckResult(OK, f"Process OK: {p.info['name']} running")
    return CheckResult(CRIT, f"Process CRITICAL: {name} not running")

