import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    # Check if inside git repo
    res = run(["git", "rev-parse", "--is-inside-work-tree"])
    if res.returncode != 0:
        logger.error("Not inside a Git repository")
        sys.exit(1)

    # Check for dirty working tree
    status = run(["git", "status", "--porcelain"])
    if status.stdout.strip():
        logger.error("Working tree is dirty. Commit or stash changes.")
        sys.exit(1)

    logger.info("Repository is clean and valid")
    sys.exit(0)

if __name__ == "__main__":
    main()
