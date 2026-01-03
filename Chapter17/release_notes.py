import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    # Get branch and commit
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    commit = run(["git", "rev-parse", "HEAD"]).stdout.strip()

    log = run([
        "git", "log",
        "--pretty=format:%h %s",
        "-5"
    ])

    if log.returncode != 0:
        logger.error("Failed to read git log")
        sys.exit(1)

    content = f"""Branch: {branch}
Commit: {commit}

Recent changes:
{log.stdout}
"""

    Path("RELEASE_NOTES.txt").write_text(content)
    logger.info("Release notes generated")

    sys.exit(0)

if __name__ == "__main__":
    main()
