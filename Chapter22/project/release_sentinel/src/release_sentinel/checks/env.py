import logging

logger = logging.getLogger(__name__)

ALLOWED_ENVS = {"dev", "stage", "prod"}

def ensure_env_allowed(env: str):
    if env not in ALLOWED_ENVS:
        raise RuntimeError(
            f"Invalid environment: {env}"
        )
