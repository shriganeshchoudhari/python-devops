import sys
import time
from kubernetes.client import V1Pod, V1ObjectMeta, V1PodSpec, V1Container
from k8s_client import load_clients, logger

POD_NAME = "python-demo-pod"
NAMESPACE = "default"

def main():
    core_v1, _ = load_clients()

    pod = V1Pod(
        metadata=V1ObjectMeta(name=POD_NAME),
        spec=V1PodSpec(
            containers=[
                V1Container(
                    name="app",
                    image="nginx:alpine"
                )
            ]
        )
    )

    try:
        core_v1.create_namespaced_pod(NAMESPACE, pod)
        logger.info("Pod created: %s", POD_NAME)

        for _ in range(20):
            p = core_v1.read_namespaced_pod(POD_NAME, NAMESPACE)
            if p.status.phase == "Running":
                logger.info("Pod is Running")
                break
            time.sleep(2)
        else:
            raise RuntimeError("Pod did not reach Running state")

    except Exception as e:
        logger.error("Pod lifecycle failed: %s", e)
        sys.exit(1)
    finally:
        core_v1.delete_namespaced_pod(POD_NAME, NAMESPACE)
        logger.info("Pod deleted")

    sys.exit(0)

if __name__ == "__main__":
    main()
