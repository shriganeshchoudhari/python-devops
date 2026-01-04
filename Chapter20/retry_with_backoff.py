import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RETRYABLE_STATUS = {429, 500, 502, 503, 504}

def get_with_retry(url, retries=3, timeout=5):
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout)

            if r.status_code == 200:
                return r.text

            if r.status_code in RETRYABLE_STATUS:
                raise RuntimeError(f"Retryable HTTP {r.status_code}")

            # Non-retryable
            raise RuntimeError(f"Non-retryable HTTP {r.status_code}")

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                RuntimeError) as e:

            if attempt == retries - 1:
                logger.error("Failed after %d attempts: %s", retries, e)
                raise

            sleep_time = 2 ** attempt
            logger.warning(
                "Attempt %d failed (%s). Retrying in %ds...",
                attempt + 1, e, sleep_time
            )
            time.sleep(sleep_time)

def main():
    get_with_retry("https://httpbin.org/status/500")

if __name__ == "__main__":
    main()
