import psutil
import logging
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("DiskMonitor")

def main():
    usage = psutil.disk_usage('/')
    percent = usage.percent
    if percent > 19:
        logger.error(f"Disk usage high: {percent}%")
        sys.exit(1)
    else:
        logger.info(f"Disk usage OK: {percent}%")
        sys.exit(0)

if __name__ == "__main__":
    main()