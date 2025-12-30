import sys
import os
import logging

# --- Configure base logger ---
logger = logging.getLogger("LoggingToolbox")
logger.setLevel(logging.DEBUG)

# Default console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# --- Assignment 1: File Checker with logging ---
def file_check(filename: str) -> int:
    if not filename:
        logger.error("Missing filename argument")
        return 2
    if os.path.exists(filename):
        logger.info("FOUND")
        return 0
    else:
        logger.error("NOT FOUND")
        return 1


# --- Assignment 2: File + Console Logger ---
def dual_logger_demo() -> int:
    # Add file handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("This message goes to console and app.log")
    logger.error("This error is logged everywhere")
    return 0


# --- Assignment 3: Exception Logging ---
def fail_fast() -> int:
    try:
        # Trigger exception
        result = 10 / 0
        logger.info(f"Result: {result}")
        return 0
    except Exception:
        logger.exception("An error occurred during fail_fast")
        return 1


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: python logging_toolbox.py <command> [args...]")
        print("Commands: check <filename>, dual-log, fail")
        sys.exit(2)

    command = sys.argv[1]

    if command == "check":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(file_check(filename))
    elif command == "dual-log":
        sys.exit(dual_logger_demo())
    elif command == "fail":
        sys.exit(fail_fast())
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)


if __name__ == "__main__":
    main()