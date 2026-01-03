import sys
import logging
import psutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def is_running(name: str) -> bool:
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == name:
            return True
    return False

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python process_check.py <process-name>")
        sys.exit(2)

    process_name = sys.argv[1]

    if not is_running(process_name):
        logger.error("Process CRITICAL: %s not running", process_name)
        sys.exit(2)

    logger.info("Process OK: %s running", process_name)
    sys.exit(0)

if __name__ == "__main__":
    main()
