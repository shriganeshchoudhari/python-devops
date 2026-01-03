import subprocess
import sys
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python tag_guard.py vX.Y.Z")
        sys.exit(1)

    version = sys.argv[1]

    if not re.match(VERSION_PATTERN, version):
        logger.error("Invalid version format: %s", version)
        sys.exit(1)

    tags = run(["git", "tag"]).stdout.splitlines()
    if version in tags:
        logger.error("Tag already exists: %s", version)
        sys.exit(1)

    logger.info("Version tag is valid: %s", version)
    sys.exit(0)

if __name__ == "__main__":
    main()
