import logging
from release_sentinel.checks.git import (
    ensure_git_repo,
    ensure_clean_tree,
    ensure_branch_allowed,
    ensure_version_valid,
    ensure_tag_not_exists,
)
from release_sentinel.checks.env import ensure_env_allowed

logger = logging.getLogger(__name__)

def run_checks(env: str, version: str) -> int:
    try:
        logger.info("Starting release validation")

        ensure_env_allowed(env)
        ensure_git_repo()
        ensure_clean_tree()
        ensure_branch_allowed()
        ensure_version_valid(version)
        ensure_tag_not_exists(version)

        logger.info("Release validation PASSED")
        return 0

    except Exception as e:
        logger.error("Release BLOCKED: %s", e)
        return 1
