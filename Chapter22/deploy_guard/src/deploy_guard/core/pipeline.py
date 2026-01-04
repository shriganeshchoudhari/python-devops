import logging, sys
from deploy_guard.core.env_gate import validate_env
from deploy_guard.core.health_checks import check_disk, check_memory
from deploy_guard.core.deploy_k8s import deploy, rollback
from deploy_guard.core.api_checks import get_with_retry
from deploy_guard.config import get_env

log = logging.getLogger("deploy_guard.pipeline")

def run_pipeline(manifest, service_url):
    # 1. Environment validation
    rc = validate_env()
    if rc != 0:
        log.error("Pipeline halted: environment validation failed")
        return rc

    # 2. Health checks
    for check in (check_disk, check_memory):
        rc = check()
        if rc == 2:
            log.error("Pipeline halted: system health critical")
            return rc

    # 3. Kubernetes apply
    rc = deploy(manifest)
    if rc != 0:
        log.error("Pipeline halted: deployment failed")
        return rc

    # 4. API health check
    rc = get_with_retry(service_url)
    if rc != 0:
        log.error("Pipeline halted: service unhealthy, triggering rollback")
        rollback(get_env("DEPLOYMENT_NAME", default="myapp"))
        return rc

    log.info("Pipeline completed successfully")
    return 0