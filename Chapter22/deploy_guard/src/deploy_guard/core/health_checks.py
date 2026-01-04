import psutil, logging
log = logging.getLogger("deploy_guard.health")

def check_disk():
    usage = psutil.disk_usage('/')
    if usage.percent >= 85:
        log.critical("Disk CRITICAL: %d%%", usage.percent)
        return 2
    elif usage.percent >= 75:
        log.warning("Disk WARN: %d%%", usage.percent)
        return 0
    log.info("Disk OK: %d%%", usage.percent)
    return 0

def check_memory():
    mem = psutil.virtual_memory()
    if mem.percent >= 85:
        log.critical("Memory CRITICAL: %d%%", mem.percent)
        return 2
    elif mem.percent >= 70:
        log.warning("Memory WARN: %d%%", mem.percent)
        return 0
    log.info("Memory OK: %d%%", mem.percent)
    return 0