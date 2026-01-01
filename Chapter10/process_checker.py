import psutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ProcessChecker")

def process_exists(name: str) -> bool:
    for proc in psutil.process_iter(attrs=['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            logger.info(f"Process '{name}' is running")
            return True
    logger.error(f"Process '{name}' not found")
    return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logger.error("Missing process name argument")
        sys.exit(1)
    exists = process_exists(sys.argv[1])
    sys.exit(0 if exists else 1)