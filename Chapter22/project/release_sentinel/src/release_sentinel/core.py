import logging
from release_sentinel.checks.git import (
    ensure_git_repo,
    ensure_clean_tree,
    ensure_branch_allowed,
    ensure_version_valid,
    ensure_tag_not_exists,
)
from release_sentinel.checks.env import ensure_env_allowed
from release_sentinel.checks.config import ensure_required_config
from release_sentinel.checks.system import (
    check_disk,
    check_memory,
    check_process,
)
from release_sentinel.checks.api import check_api
from release_sentinel.checks.result import CRIT

logger = logging.getLogger(__name__)

def run_checks(env: str, version: str) -> int:
    try:
        logger.info("Starting release validation")

        # Phase 2 — policy gates
        ensure_env_allowed(env)
        ensure_git_repo()
        ensure_clean_tree()
        ensure_branch_allowed()
        ensure_version_valid(version)
        ensure_tag_not_exists(version)

        # Phase 4 — config & secrets gate
        cfg = ensure_required_config()

        # Phase 3 — health gates (now config-driven)
        results = [
            check_disk(),
            check_memory(),
            check_process(cfg["process"]),
            check_api(cfg["api_url"]),
        ]

        exit_code = 0
        for r in results:
            if r.status == CRIT:
                logger.error(r.message)
                exit_code = 2
            else:
                logger.info(r.message)

        if exit_code == 0:
            logger.info("Release validation PASSED")
        else:
            logger.error("Release BLOCKED: critical health check failed")

        return exit_code

    except Exception as e:
        logger.error("Release BLOCKED: %s", e)
        return 1
