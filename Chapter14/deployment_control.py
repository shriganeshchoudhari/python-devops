import sys
from kubernetes.client import (
    V1Deployment, V1DeploymentSpec,
    V1LabelSelector, V1PodTemplateSpec,
    V1PodSpec, V1Container, V1ObjectMeta
)
from k8s_client import load_clients, logger

NAME = "python-deploy"
NAMESPACE = "default"

def main():
    _, apps_v1 = load_clients()

    deployment = V1Deployment(
        metadata=V1ObjectMeta(name=NAME),
        spec=V1DeploymentSpec(
            replicas=2,
            selector=V1LabelSelector(match_labels={"app": "demo"}),
            template=V1PodTemplateSpec(
                metadata=V1ObjectMeta(labels={"app": "demo"}),
                spec=V1PodSpec(
                    containers=[
                        V1Container(
                            name="app",
                            image="nginx:alpine"
                        )
                    ]
                )
            )
        )
    )

    try:
        apps_v1.create_namespaced_deployment(NAMESPACE, deployment)
        logger.info("Deployment created with 2 replicas")

        dep = apps_v1.read_namespaced_deployment(NAME, NAMESPACE)
        dep.spec.replicas = 3

        apps_v1.patch_namespaced_deployment(NAME, NAMESPACE, dep)
        logger.info("Deployment scaled to 3 replicas")

        updated = apps_v1.read_namespaced_deployment(NAME, NAMESPACE)
        logger.info("Verified replicas: %s", updated.spec.replicas)

        sys.exit(0)

    except Exception as e:
        logger.error("Deployment control failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
