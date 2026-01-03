import sys
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    load_dotenv()  # loads .env into environment

    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API_KEY not found in .env")
        sys.exit(1)

    logger.info("API_KEY loaded from .env safely")
    sys.exit(0)

if __name__ == "__main__":
    main()
