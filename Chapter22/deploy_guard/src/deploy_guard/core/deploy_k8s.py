import subprocess, logging, sys
log = logging.getLogger("deploy_guard.k8s")

def run_cmd(cmd):
    try:
        subprocess.check_call(cmd)
        return 0
    except subprocess.CalledProcessError as e:
        log.error("Command failed: %s", cmd)
        return 2

def deploy(manifest):
    # Dry-run first
    rc = run_cmd(["kubectl", "apply", "--dry-run=server", "-f", manifest])
    if rc != 0:
        log.error("Dry-run failed")
        return 2

    # Real apply
    rc = run_cmd(["kubectl", "apply", "-f", manifest])
    if rc != 0:
        log.error("Apply failed")
        return 2

    log.info("Deployment applied successfully: %s", manifest)
    return 0

def rollback(deployment, namespace="default"):
    rc = run_cmd(["kubectl", "rollout", "undo", f"deployment/{deployment}", "-n", namespace])
    if rc == 0:
        log.info("Rollback executed for %s", deployment)
    else:
        log.error("Rollback failed for %s", deployment)
    return rc