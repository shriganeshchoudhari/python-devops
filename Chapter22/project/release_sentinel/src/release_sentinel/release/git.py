import subprocess
import logging

logger = logging.getLogger(__name__)

def _run(cmd):
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

def create_and_push_tag(version: str):
    # Check if tag already exists (idempotency)
    tags = _run(["git", "tag"]).stdout.splitlines()
    if version in tags:
        raise RuntimeError(f"Tag already exists: {version}")

    # Create annotated tag
    res = _run([
        "git", "tag", "-a", version, "-m", f"Release {version}"
    ])
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip())

    # Push tag
    res = _run(["git", "push", "origin", version])
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip())

    logger.info("Git tag %s created and pushed", version)
