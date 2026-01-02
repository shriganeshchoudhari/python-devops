import sys
from kubernetes.client import (
    V1Deployment, V1DeploymentSpec,
    V1LabelSelector, V1PodTemplateSpec,
    V1PodSpec, V1Container, V1ObjectMeta
)
from kubernetes.client.exceptions import ApiException
from k8s_client import load_clients, logger

NAMESPACE = "default"

def ensure_deployment(name, image, replicas):
    _, apps_v1 = load_clients()

    try:
        dep = apps_v1.read_namespaced_deployment(name, NAMESPACE)
        logger.info("Deployment exists, updating")

        dep.spec.replicas = replicas
        dep.spec.template.spec.containers[0].image = image

        apps_v1.patch_namespaced_deployment(name, NAMESPACE, dep)

    except ApiException as e:
        if e.status != 404:
            raise

        logger.info("Deployment not found, creating")

        deployment = V1Deployment(
            metadata=V1ObjectMeta(name=name),
            spec=V1DeploymentSpec(
                replicas=replicas,
                selector=V1LabelSelector(match_labels={"app": name}),
                template=V1PodTemplateSpec(
                    metadata=V1ObjectMeta(labels={"app": name}),
                    spec=V1PodSpec(
                        containers=[
                            V1Container(
                                name="app",
                                image=image
                            )
                        ]
                    )
                )
            )
        )

        apps_v1.create_namespaced_deployment(NAMESPACE, deployment)

    final = apps_v1.read_namespaced_deployment(name, NAMESPACE)
    if final.spec.replicas != replicas:
        raise RuntimeError("Replica verification failed")

    logger.info(
        "Deployment ensured: %s | image=%s | replicas=%d",
        name, image, replicas
    )

def main():
    try:
        ensure_deployment("safe-deploy", "nginx:alpine", 2)
        sys.exit(0)
    except Exception as e:
        logger.error("Ensure deployment failed: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
