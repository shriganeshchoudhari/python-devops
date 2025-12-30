import sys
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def main():
    if len(sys.argv) < 2:
        logging.error("Missing filename argument")
        sys.exit(2)

    filename = sys.argv[1]

    if os.path.exists(filename):
        logging.info("FOUND")
        sys.exit(0)
    else:
        logging.error("NOT FOUND")
        sys.exit(1)

if __name__ == "__main__":
    main()