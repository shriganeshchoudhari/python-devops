import requests
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_with_timeout(url, timeout=5):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.exceptions.Timeout:
        logger.error("Request timed out after %s seconds", timeout)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
        sys.exit(1)

def main():
    fetch_with_timeout("https://httpbin.org/delay/10", timeout=3)

if __name__ == "__main__":
    main()
