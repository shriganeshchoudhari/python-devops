import sys
from k8s_client import load_clients, logger

def main():
    try:
        core_v1, _ = load_clients()

        logger.info("Namespaces:")
        for ns in core_v1.list_namespace().items:
            logger.info(" - %s", ns.metadata.name)

        logger.info("Pods:")
        pods = core_v1.list_pod_for_all_namespaces()
        for p in pods.items:
            logger.info(
                "%s/%s -> %s",
                p.metadata.namespace,
                p.metadata.name,
                p.status.phase
            )

        sys.exit(0)
    except Exception as e:
        logger.error("Cluster inspection failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
