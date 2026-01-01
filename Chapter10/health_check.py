import psutil
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("HealthCheck")

def check_disk(threshold=80):
    usage = psutil.disk_usage('/')
    percent = usage.percent
    if percent > threshold:
        logger.error(f"Disk usage high: {percent}%")
        return False
    logger.info(f"Disk usage OK: {percent}%")
    return True

def check_memory(threshold=75):
    mem = psutil.virtual_memory()
    percent = mem.percent
    if percent > threshold:
        logger.error(f"Memory usage high: {percent}%")
        return False
    logger.info(f"Memory usage OK: {percent}%")
    return True

def check_process(name: str):
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            logger.info(f"Process '{name}' is running")
            return True
    logger.error(f"Process '{name}' not found")
    return False

def main():
    # Example: check disk, memory, and a process (like 'python')
    disk_ok = check_disk()
    mem_ok = check_memory()
    proc_ok = check_process("python")

    if not (disk_ok and mem_ok and proc_ok):
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()