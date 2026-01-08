import os

ALLOWED_ENVS = {"dev", "stage", "prod"}

def get_env(name: str, default=None, required: bool = False, secret: bool = False):
    val = os.getenv(name, default)
    if required and val is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

def normalize_env(value: str) -> str:
    return value.strip().lower()