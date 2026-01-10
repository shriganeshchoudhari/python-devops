import logging
import os

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
from release_sentinel.release.notes import generate_notes
from release_sentinel.metrics import write_metric

logger = logging.getLogger(__name__)


def run_checks(env: str, version: str) -> int:
    """
    Exit codes:
      0 = SAFE
      1 = BLOCKED (policy/config failure)
      2 = CRITICAL (runtime health failure)
    """
    try:
        logger.info("Starting release validation")

        # -------------------------
        # Environment policy
        # -------------------------
        ensure_env_allowed(env)

        skip_git = os.getenv("RS_SKIP_GIT_CHECKS", "").lower() == "true"

        # -------------------------
        # Git policy checks (CI / local)
        # -------------------------
        if not skip_git:
            ensure_git_repo()
            ensure_clean_tree()
            ensure_branch_allowed()
            ensure_version_valid(version)
            ensure_tag_not_exists(version)
        else:
            logger.info("Skipping Git checks (runtime environment)")

        # -------------------------
        # Config & secrets
        # -------------------------
        cfg = ensure_required_config()

        # -------------------------
        # Runtime health checks
        # -------------------------
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

        # -------------------------
        # CRITICAL failure path
        # -------------------------
        if exit_code == 2:
            msg = "Release BLOCKED (CRITICAL): system or dependency unhealthy"
            logger.error(msg)
            send_webhook(msg, severity="CRITICAL")

            write_metric(
                "release_sentinel_status",
                0,
                {"result": "critical", "env": env}
            )
            return 2

        # -------------------------
        # SUCCESS path
        # -------------------------
        logger.info("Release validation PASSED")

        write_metric(
            "release_sentinel_status",
            1,
            {"result": "safe", "env": env}
        )

        # Release actions ONLY where Git context exists (CI)
        if not skip_git:
            notes = generate_notes(version)
            create_and_push_tag(version)
            create_github_release(version, notes)
        else:
            logger.info("Skipping release creation (runtime mode)")

        return 0

    # -------------------------
    # POLICY / CONFIG failure
    # -------------------------
    except Exception as e:
        msg = f"Release BLOCKED (policy): {e}"
        logger.error(msg)
        send_webhook(msg, severity="BLOCKED")

        write_metric(
            "release_sentinel_status",
            0,
            {"result": "blocked", "env": env}
        )
        return 1
