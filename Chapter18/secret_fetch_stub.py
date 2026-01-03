import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_secret():
    token = os.getenv("VAULT_TOKEN")

    if not token:
        raise RuntimeError("VAULT_TOKEN not set")

    # Simulated secure fetch
    # In real life, this would be an API call
    secret = "fetched-secret-value"

    return secret

def main():
    try:
        _ = fetch_secret()
        logger.info("Secret fetched successfully")
        sys.exit(0)
    except Exception as e:
        logger.error("Secret fetch failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
