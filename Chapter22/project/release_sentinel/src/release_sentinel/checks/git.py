import subprocess
import logging
import re

logger = logging.getLogger(__name__)

SEMVER_PATTERN = r"^v\d+\.\d+\.\d+$"
ALLOWED_BRANCHES = {"main", "master"}

def _run(cmd):
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

def ensure_git_repo():
    res = _run(["git", "rev-parse", "--is-inside-work-tree"])
    if res.returncode != 0:
        raise RuntimeError("Not inside a Git repository")

def ensure_clean_tree():
    res = _run(["git", "status", "--porcelain"])
    if res.stdout.strip():
        raise RuntimeError("Git working tree is dirty")

def ensure_branch_allowed():
    branch = _run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    ).stdout.strip()

    if branch not in ALLOWED_BRANCHES:
        raise RuntimeError(
            f"Releases blocked from branch: {branch}"
        )

def ensure_version_valid(version: str):
    if not re.match(SEMVER_PATTERN, version):
        raise RuntimeError(
            f"Invalid version format: {version}"
        )

def ensure_tag_not_exists(version: str):
    tags = _run(["git", "tag"]).stdout.splitlines()
    if version in tags:
        raise RuntimeError(
            f"Git tag already exists: {version}"
        )
