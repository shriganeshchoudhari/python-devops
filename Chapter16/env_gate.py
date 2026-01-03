import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ALLOWED_ENVS = {"dev", "stage", "prod"}

def main():
    env = os.getenv("ENV")

    if not env:
        logger.error("ENV variable is not set")
        sys.exit(1)

    if env not in ALLOWED_ENVS:
        logger.error("Invalid ENV value: %s", env)
        sys.exit(1)

    logger.info("ENV validated: %s", env)
    sys.exit(0)

if __name__ == "__main__":
    main()
