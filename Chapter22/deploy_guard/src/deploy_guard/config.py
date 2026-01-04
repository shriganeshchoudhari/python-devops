import os

def get_env(name: str, default=None, required=False, secret=False):
    """
    Centralized environment variable loader.
    - required=True → raises RuntimeError if missing
    - secret=True → never log the value
    """
    value = os.getenv(name, default)
    if required and value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return value