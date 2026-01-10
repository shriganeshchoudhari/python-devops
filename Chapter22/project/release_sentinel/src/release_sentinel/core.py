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

from release_sentinel.alerts.webhook import send_webhook
from release_sentinel.release.git import create_and_push_tag
from release_sentinel.release.github import create_github_release

logger = logging.getLogger(__name__)


def run_checks(env: str, version: str) -> int:
    """
    Exit codes:
      0 = SAFE (release created)
      1 = BLOCKED (policy/config failure)
      2 = CRITICAL (runtime health failure)
    """
    try:
        logger.info("Starting release validation")

        # -------------------------
        # Phase 2 — Policy gates
        # -------------------------
        ensure_env_allowed(env)
        ensure_git_repo()
        ensure_clean_tree()
        ensure_branch_allowed()
        ensure_version_valid(version)
        ensure_tag_not_exists(version)

        # -------------------------
        # Phase 4 — Config & secrets
        # -------------------------
        cfg = ensure_required_config()

        # -------------------------
        # Phase 3 — Runtime health
        # -------------------------
        results = [
            check_disk(),
            check_memory(),
            check_process(cfg["process"]),
            check_api(cfg["api_url"]),
        ]

        exit_code = 0

        for result in results:
            if result.status == CRIT:
                logger.error(result.message)
                exit_code = 2
            else:
                logger.info(result.message)

        if exit_code != 0:
            msg = "Release BLOCKED (CRITICAL): system or dependency unhealthy"
            logger.error(msg)
            send_webhook(msg, severity="CRITICAL")
            return exit_code

        # -------------------------
        # SUCCESS — Release allowed
        # -------------------------
        logger.info("Release validation PASSED")

        # These MUST fail hard if they fail
        create_and_push_tag(version)
        create_github_release(version)

        logger.info("Release %s completed successfully", version)
        return 0

    except Exception as e:
        msg = f"Release BLOCKED (policy): {e}"
        logger.error(msg)
        send_webhook(msg, severity="BLOCKED")
        return 1
