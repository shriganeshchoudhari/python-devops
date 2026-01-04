import subprocess, logging, re
log = logging.getLogger("deploy_guard.release")

def create_tag(version):
    if not re.match(r"^v\d+\.\d+\.\d+$", version):
        log.error("Invalid version format: %s", version)
        return 2
    try:
        subprocess.check_call(["git", "tag", "-a", version, "-m", f"Release {version}"])
        log.info("Tag created: %s", version)
        return 0
    except subprocess.CalledProcessError as e:
        log.error("Failed to create tag: %s", e)
        return 2