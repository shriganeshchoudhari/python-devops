import logging
from deploy_guard.config import get_env

log = logging.getLogger("deploy_guard.env")

ALLOWED_ENVS = {"dev", "stage", "prod"}

def validate_env():
    env = get_env("ENV", required=True).strip().lower()
    if env not in ALLOWED_ENVS:
        log.error("Invalid ENV: %s", env)
        return 2

    try:
        # Required secrets/config
        get_env("KUBECONFIG", required=True, secret=True)
        get_env("SERVICE_URL", required=True)
        get_env("VERSION", required=True)
    except RuntimeError as e:
        log.error(str(e))
        return 2

    log.info("Environment validated: %s", env)
    return 0