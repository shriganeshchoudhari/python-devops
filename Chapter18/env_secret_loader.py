import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    api_key = os.getenv("API_KEY")

    if not api_key:
        logger.error("API_KEY is not set")
        sys.exit(1)

    logger.info("API_KEY loaded successfully")
    sys.exit(0)

if __name__ == "__main__":
    main()
