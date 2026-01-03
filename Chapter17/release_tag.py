import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run(cmd, fail_msg):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        logger.error("%s\n%s", fail_msg, res.stderr.strip())
        sys.exit(1)
    return res.stdout.strip()

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python release_tag.py vX.Y.Z")
        sys.exit(1)

    version = sys.argv[1]

    # Repo guard
    run(["git", "rev-parse", "--is-inside-work-tree"], "Not a git repo")

    if run(["git", "status", "--porcelain"], "").strip():
        logger.error("Working tree is dirty")
        sys.exit(1)

    # Tag guard
    tags = run(["git", "tag"], "").splitlines()
    if version in tags:
        logger.error("Tag already exists: %s", version)
        sys.exit(1)

    # Create annotated tag
    run(
        ["git", "tag", "-a", version, "-m", f"Release {version}"],
        "Failed to create tag"
    )

    # Push tag
    run(
        ["git", "push", "origin", version],
        "Failed to push tag"
    )

    logger.info("Release %s created and pushed successfully", version)
    sys.exit(0)

if __name__ == "__main__":
    main()
