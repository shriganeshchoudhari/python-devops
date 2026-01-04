import requests
import logging
import sys
import time
import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ResilienceToolbox")


# --- Assignment 1: Timeout Wrapper ---
def call_with_timeout(url, timeout=5):
    try:
        resp = requests.get(url, timeout=timeout)
        logger.info("Request succeeded: %s", resp.status_code)
        return 0
    except requests.exceptions.Timeout:
        logger.error("Request timed out after %s seconds", timeout)
        return 1
    except Exception as e:
        logger.error("Request failed: %s", e)
        return 1


# --- Assignment 2: Retry with Backoff ---
def get_with_retry(url, max_attempts=3):
    attempt = 0
    backoff = 1
    while attempt < max_attempts:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code >= 500:
                raise requests.exceptions.RequestException(f"Server error {resp.status_code}")
            logger.info("Request succeeded on attempt %d", attempt + 1)
            return 0
        except requests.exceptions.RequestException as e:
            attempt += 1
            if attempt >= max_attempts:
                logger.error("Final failure after %d attempts: %s", attempt, e)
                return 1
            logger.warning("Attempt %d failed: %s. Retrying in %d seconds...", attempt, e, backoff)
            time.sleep(backoff)
            backoff *= 2


# --- Assignment 3: Idempotent File Creator ---
def create_file(path, content="Hello World"):
    if os.path.exists(path):
        logger.info("File already exists: %s (no action taken)", path)
        return 0
    with open(path, "w") as f:
        f.write(content)
    logger.info("File created: %s", path)
    return 0


# --- Assignment 4: Idempotent Action Guard ---
resources = set()

def safe_create(resource_id):
    if resource_id in resources:
        logger.info("Resource %s already exists (no action taken)", resource_id)
        return 0
    resources.add(resource_id)
    logger.info("Resource %s created successfully", resource_id)
    return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: resilience_toolbox.py [timeout <url>|retry <url>|file <path>|safe <id>]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "timeout":
        if len(sys.argv) < 3:
            logger.error("Missing URL argument")
            sys.exit(1)
        sys.exit(call_with_timeout(sys.argv[2]))
    elif cmd == "retry":
        if len(sys.argv) < 3:
            logger.error("Missing URL argument")
            sys.exit(1)
        sys.exit(get_with_retry(sys.argv[2]))
    elif cmd == "file":
        if len(sys.argv) < 3:
            logger.error("Missing file path argument")
            sys.exit(1)
        sys.exit(create_file(sys.argv[2]))
    elif cmd == "safe":
        if len(sys.argv) < 3:
            logger.error("Missing resource ID argument")
            sys.exit(1)
        sys.exit(safe_create(sys.argv[2]))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()