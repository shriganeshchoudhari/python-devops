import sys
import os
import logging
import requests
from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.INFO: Fore.GREEN,
        logging.ERROR: Fore.RED,
        logging.WARNING: Fore.YELLOW,
        logging.DEBUG: Fore.CYAN,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

# --- Configure logger ---
logger = logging.getLogger("APIToolbox")
logger.setLevel(logging.DEBUG)

# Console handler with colors
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = ColorFormatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

# File handler (no colors, full logs)
file_handler = logging.FileHandler("api.log")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)

# Attach handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# --- Assignment 1: Public API Call ---
def api_call() -> int:
    url = "https://api.github.com"
    try:
        response = requests.get(url, timeout=5)
        logger.info(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Field current_user_url: {data.get('current_user_url')}")
            return 0
        else:
            logger.error("API call failed")
            return 1
    except requests.exceptions.RequestException as e:
        logger.error(f"Error: {e}")
        return 1


# --- Assignment 2: Status Code Validator ---
def check_api(url: str):
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception(f"API call failed with status {response.status_code}")
    return response.json()

def api_validate() -> int:
    try:
        data = check_api("https://api.github.com")
        logger.info("API OK, got keys: %s", list(data.keys())[:5])
        return 0
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return 1


# --- Assignment 3: Token Safety ---
def token_safety() -> int:
    token = os.environ.get("API_TOKEN")
    if not token:
        logger.error("API_TOKEN missing in environment")
        return 1
    logger.info("Token loaded")
    return 0


# --- Help Subcommand ---
def show_help() -> int:
    help_text = """
API Toolbox — Available Commands:

  call       : Call https://api.github.com, print status + one JSON field.
  validate   : Validate API status code (200 OK) and show JSON keys.
  token      : Check API_TOKEN env variable, log error if missing.
  help       : Show this usage guide.

Exit Codes:
  0 : Success
  1 : Error
  2 : Missing arguments / Unknown command
"""
    print(help_text.strip())
    return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(2)

    command = sys.argv[1]

    if command == "call":
        sys.exit(api_call())
    elif command == "validate":
        sys.exit(api_validate())
    elif command == "token":
        sys.exit(token_safety())
    elif command == "help":
        sys.exit(show_help())
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)


if __name__ == "__main__":
    main()