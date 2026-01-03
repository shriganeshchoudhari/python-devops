import psutil
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("HealthToolbox")


# --- Assignment 1: Disk Health ---
def check_disk():
    usage = psutil.disk_usage('/')
    percent = usage.percent
    if percent >= 85:
        logger.critical("Disk usage CRITICAL: %d%%", percent)
        return 2
    elif percent >= 75:
        logger.warning("Disk usage WARN: %d%%", percent)
        return 0
    else:
        logger.info("Disk usage OK: %d%%", percent)
        return 0


# --- Assignment 2: Memory Health ---
def check_memory():
    mem = psutil.virtual_memory()
    percent = mem.percent
    if percent >= 85:
        logger.critical("Memory usage CRITICAL: %d%%", percent)
        return 2
    elif percent >= 70:
        logger.warning("Memory usage WARN: %d%%", percent)
        return 0
    else:
        logger.info("Memory usage OK: %d%%", percent)
        return 0


# --- Assignment 3: Process Monitor ---
def check_process(name):
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            logger.info("Process '%s' is running", name)
            return 0
    logger.critical("Process '%s' not running", name)
    return 2


# --- Assignment 4: Composite Health ---
def composite(process_name):
    results = [check_disk(), check_memory(), check_process(process_name)]

    if 2 in results:
        logger.critical("Composite check: CRITICAL failure detected")
        return 2
    elif any(r == 0 for r in results):
        logger.warning("Composite check: WARN detected")
        return 0
    else:
        logger.info("Composite check: All OK")
        return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: health_toolbox.py [disk|memory|process <name>|composite <name>]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "disk":
        sys.exit(check_disk())
    elif cmd == "memory":
        sys.exit(check_memory())
    elif cmd == "process":
        if len(sys.argv) < 3:
            logger.error("Missing process name argument")
            sys.exit(2)
        sys.exit(check_process(sys.argv[2]))
    elif cmd == "composite":
        if len(sys.argv) < 3:
            logger.error("Missing process name argument")
            sys.exit(2)
        sys.exit(composite(sys.argv[2]))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()