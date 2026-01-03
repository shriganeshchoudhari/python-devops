import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

REQUIRED_FILES = [
    "Dockerfile",
    "requirements.txt"
]

def main():
    missing = []

    for file in REQUIRED_FILES:
        if not Path(file).exists():
            missing.append(file)

    if missing:
        for f in missing:
            logger.error("Missing required file: %s", f)
        sys.exit(1)

    logger.info("All required files are present")
    sys.exit(0)

if __name__ == "__main__":
    main()
