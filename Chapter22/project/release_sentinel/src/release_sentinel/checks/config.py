import logging
from release_sentinel.config import get_env

logger = logging.getLogger(__name__)

def ensure_required_config():
    process = get_env("RS_REQUIRED_PROCESS", required=True)
    api_url = get_env("RS_API_URL", required=True)
    token = get_env("RS_DEPLOY_TOKEN", required=True)

    # NEVER log secrets
    logger.info("Config OK: process=%s, api_url=%s", process, api_url)

    return {
        "process": process,
        "api_url": api_url,
        "token": token,  # used later, not logged
    }
