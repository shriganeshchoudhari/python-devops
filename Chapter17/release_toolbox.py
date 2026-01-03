import subprocess
import logging
import sys
import re

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ReleaseToolbox")


# --- Repo Guard ---
def repo_guard():
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
    except subprocess.CalledProcessError:
        logger.error("Not inside a Git repository")
        return 1

    status = subprocess.check_output(["git", "status", "--porcelain"]).decode().strip()
    if status:
        logger.error("Working tree is dirty")
        return 1

    logger.info("Repo is clean and valid")
    return 0


# --- Tag Guard ---
def tag_guard(version):
    pattern = r"^v\d+\.\d+\.\d+$"
    if not re.match(pattern, version):
        logger.error("Invalid version format: %s", version)
        return 1

    tags = subprocess.check_output(["git", "tag"]).decode().splitlines()
    if version in tags:
        logger.error("Tag already exists: %s", version)
        return 1

    logger.info("Tag is valid and does not exist: %s", version)
    return 0


# --- Release Tagger ---
def release_tag(version):
    if repo_guard() != 0:
        return 1
    if tag_guard(version) != 0:
        return 1

    try:
        subprocess.check_call(["git", "tag", "-a", version, "-m", f"Release {version}"])
        logger.info("Created tag: %s", version)
        subprocess.check_call(["git", "push", "origin", version])
        logger.info("Pushed tag to origin: %s", version)
        return 0
    except subprocess.CalledProcessError as e:
        logger.error("Release tagging failed: %s", e)
        return 1


# --- Release Notes ---
def release_notes(n=5):
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        commits = subprocess.check_output(
            ["git", "log", f"-{n}", "--pretty=format:%h %s"]).decode().splitlines()

        with open("RELEASE_NOTES.txt", "w") as f:
            f.write(f"Branch: {branch}\n")
            f.write("Recent commits:\n")
            for c in commits:
                f.write(c + "\n")

        logger.info("Release notes written to RELEASE_NOTES.txt")
        return 0
    except subprocess.CalledProcessError as e:
        logger.error("Failed to generate release notes: %s", e)
        return 1


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: release_toolbox.py [guard|tag <vX.Y.Z>|release <vX.Y.Z>|notes <N>]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "guard":
        sys.exit(repo_guard())
    elif cmd == "tag":
        if len(sys.argv) < 3:
            logger.error("Missing version argument")
            sys.exit(1)
        sys.exit(tag_guard(sys.argv[2]))
    elif cmd == "release":
        if len(sys.argv) < 3:
            logger.error("Missing version argument")
            sys.exit(1)
        sys.exit(release_tag(sys.argv[2]))
    elif cmd == "notes":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        sys.exit(release_notes(n))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()