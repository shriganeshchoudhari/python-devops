import logging
import sys

# Configure logger
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("ExceptionLogger")

def main():
    try:
        # Trigger an exception (division by zero)
        result = 10 / 0
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.exception("An error occurred")
        sys.exit(1)

if __name__ == "__main__":
    main()