import sys
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python version_gate.py vX.Y.Z")
        sys.exit(1)

    version = sys.argv[1]

    if not re.match(VERSION_PATTERN, version):
        logger.error("Invalid version format: %s", version)
        sys.exit(1)

    logger.info("Version validated: %s", version)
    sys.exit(0)

if __name__ == "__main__":
    main()
