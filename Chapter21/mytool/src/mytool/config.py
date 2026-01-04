import os

def get_env(name: str, default=None, required=False):
    value = os.getenv(name, default)
    if required and value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return value
