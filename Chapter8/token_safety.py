import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    token = os.environ.get("API_TOKEN")

    if not token:
        logging.error("API_TOKEN missing in environment")
        sys.exit(1)

    logging.info("Token loaded")
    sys.exit(0)

if __name__ == "__main__":
    main()