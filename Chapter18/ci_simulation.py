import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    token = os.getenv("DEPLOY_TOKEN")

    if not token:
        logger.error("DEPLOY_TOKEN missing — CI must stop")
        sys.exit(1)

    logger.info("DEPLOY_TOKEN detected (value not logged)")
    sys.exit(0)

if __name__ == "__main__":
    main()
