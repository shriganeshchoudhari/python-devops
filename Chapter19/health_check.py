import sys
import logging
import shutil
import psutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

DISK_WARN = 75
DISK_CRIT = 85
MEM_WARN = 70
MEM_CRIT = 85
PROCESS_NAME = "python"  # example

def check_disk():
    total, used, _ = shutil.disk_usage("/")
    pct = (used / total) * 100
    if pct >= DISK_CRIT:
        return "CRIT", f"Disk {pct:.1f}%"
    if pct >= DISK_WARN:
        return "WARN", f"Disk {pct:.1f}%"
    return "OK", f"Disk {pct:.1f}%"

def check_memory():
    pct = psutil.virtual_memory().percent
    if pct >= MEM_CRIT:
        return "CRIT", f"Memory {pct:.1f}%"
    if pct >= MEM_WARN:
        return "WARN", f"Memory {pct:.1f}%"
    return "OK", f"Memory {pct:.1f}%"

def check_process():
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == PROCESS_NAME:
            return "OK", f"Process {PROCESS_NAME} running"
    return "CRIT", f"Process {PROCESS_NAME} not running"

def main():
    checks = [
        check_disk(),
        check_memory(),
        check_process()
    ]

    has_crit = False
    has_warn = False

    for status, msg in checks:
        if status == "CRIT":
            logger.error(msg)
            has_crit = True
        elif status == "WARN":
            logger.warning(msg)
            has_warn = True
        else:
            logger.info(msg)

    if has_crit:
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
