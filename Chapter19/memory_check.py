import psutil
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

WARN_THRESHOLD = 75
CRIT_THRESHOLD = 85

def main():
    mem_pct = psutil.virtual_memory().percent

    if mem_pct >= CRIT_THRESHOLD:
        logger.error("Memory CRITICAL: %.1f%% used", mem_pct)
        sys.exit(2)

    if mem_pct >= WARN_THRESHOLD:
        logger.warning("Memory WARNING: %.1f%% used", mem_pct)
        sys.exit(0)

    logger.info("Memory OK: %.1f%% used", mem_pct)
    sys.exit(0)

if __name__ == "__main__":
    main()
