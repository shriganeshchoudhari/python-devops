import os
import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("SecretsToolbox")


# --- Assignment 1: Env Secret Loader ---
def load_env_secret():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        logger.error("Missing API_KEY in environment")
        return 1
    logger.info("API_KEY loaded successfully (value hidden)")
    return 0


# --- Assignment 2: .env Safety ---
def load_dotenv_secret():
    if not os.path.exists(".env"):
        logger.error(".env file missing — secrets not loaded")
        return 1

    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if not api_key:
        logger.error("API_KEY missing in .env")
        return 1

    logger.info("Secrets loaded from .env (values hidden)")
    return 0


# --- Assignment 3: CI Simulation ---
def ci_simulation():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        logger.error("CI Simulation failed — API_KEY not set")
        return 1
    logger.info("CI Simulation success — API_KEY present (value hidden)")
    return 0


# --- Assignment 4: Secret Fetch Stub ---
def fetch_secret():
    token = os.environ.get("TOKEN")
    if not token:
        logger.error("Missing TOKEN in environment")
        return None

    # Simulate API fetch without revealing token
    logger.info("Fetched secret successfully (value hidden)")
    return {"status": "ok", "data": "simulated response"}


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: secrets_toolbox.py [load|dotenv|ci|fetch]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "load":
        sys.exit(load_env_secret())
    elif cmd == "dotenv":
        sys.exit(load_dotenv_secret())
    elif cmd == "ci":
        sys.exit(ci_simulation())
    elif cmd == "fetch":
        result = fetch_secret()
        sys.exit(0 if result else 1)
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()