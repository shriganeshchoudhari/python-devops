# src/mytool/cli.py
import sys
import argparse
import logging
from mytool.logging import setup_logging
from mytool.core import calculate_disk_percentage

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Disk usage calculator")
    parser.add_argument("--used", type=int, required=True)
    parser.add_argument("--total", type=int, required=True)
    args = parser.parse_args()

    try:
        pct = calculate_disk_percentage(args.used, args.total)
        logging.getLogger("mytool").info("Disk usage: %.1f%%", pct)
        sys.exit(0)
    except Exception as e:
        logging.getLogger("mytool").error("ERROR: %s", e)
        sys.exit(1)