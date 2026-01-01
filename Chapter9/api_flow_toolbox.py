import sys
import time
import requests
import logging

# --- Configure logger ---
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("APIFlowToolbox")


# --- Assignment 1: Pagination Simulator ---
def paginate() -> int:
    pages = [
        ["item1", "item2"],
        ["item3", "item4"],
        ["item5"]
    ]
    all_items = []
    for page in pages:
        all_items.extend(page)

    logger.info("Total items collected: %d", len(all_items))
    logger.info("Items: %s", all_items)
    return 0


# --- Assignment 2: Retry Wrapper ---
def get_with_retry(url, retries=3, timeout=5):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning("Attempt %d failed: %s", attempt, e)
            last_error = e
            time.sleep(1)
    raise RuntimeError(f"Failed after {retries} retries") from last_error

def retry_demo(url: str) -> int:
    try:
        resp = get_with_retry(url)
        logger.info("Success: %s", resp.status_code)
        return 0
    except Exception as e:
        logger.error("Final error: %s", e)
        return 1


# --- Assignment 3: Rate Limit Handler ---
def rate_limit_handler(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", "1"))
            logger.warning("Rate limited. Retrying after %d seconds...", retry_after)
            time.sleep(retry_after)
            response = requests.get(url, timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        logger.error("Error: %s", e)
        return None

def ratelimit_demo(url: str) -> int:
    resp = rate_limit_handler(url)
    if resp:
        logger.info("Final status: %s", resp.status_code)
        return 0
    return 1


# --- Help Subcommand ---
def show_help() -> int:
    help_text = """
API Flow Toolbox — Available Commands:

  paginate             : Simulate pagination (3 pages), collect items, print total count.
  retry [--url <url>]  : Demonstrate retry wrapper with timeout and error handling.
                         Default: https://api.github.com
  ratelimit [--url <url>] : Handle 429 Too Many Requests, respect Retry-After, retry once.
                            Default: https://httpbin.org/status/429
  help                 : Show this usage guide.

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

    if command == "paginate":
        sys.exit(paginate())
    elif command == "retry":
        url = "https://api.github.com"
        if "--url" in sys.argv:
            idx = sys.argv.index("--url")
            if idx + 1 < len(sys.argv):
                url = sys.argv[idx + 1]
        sys.exit(retry_demo(url))
    elif command == "ratelimit":
        url = "https://httpbin.org/status/429"
        if "--url" in sys.argv:
            idx = sys.argv.index("--url")
            if idx + 1 < len(sys.argv):
                url = sys.argv[idx + 1]
        sys.exit(ratelimit_demo(url))
    elif command == "help":
        sys.exit(show_help())
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)


if __name__ == "__main__":
    main()