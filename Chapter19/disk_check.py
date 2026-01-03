import shutil
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
    total, used, free = shutil.disk_usage("/")
    usage_pct = (used / total) * 100

    if usage_pct >= CRIT_THRESHOLD:
        logger.error("Disk CRITICAL: %.1f%% used", usage_pct)
        sys.exit(2)

    if usage_pct >= WARN_THRESHOLD:
        logger.warning("Disk WARNING: %.1f%% used", usage_pct)
        sys.exit(0)

    logger.info("Disk OK: %.1f%% used", usage_pct)
    sys.exit(0)

if __name__ == "__main__":
    main()
