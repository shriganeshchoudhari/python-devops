You want **solutions**, not theory. Good.
Below is **clean, safe, production-style code** for **ALL Chapter 14 assignments** using the **official Kubernetes Python client**.

I’m not optimizing for “short”. I’m optimizing for **correct cluster behavior**.

---

# ✅ CHAPTER 14 — KUBERNETES AUTOMATION (SOLUTIONS)

## 📁 Recommended Structure

```
chapter14/
├── k8s_client.py
├── cluster_inspect.py
├── pod_lifecycle.py
├── deployment_control.py
└── ensure_deployment.py
```

All scripts assume:

* `kubectl` already works
* kubeconfig present
* default namespace (explicitly used)

---

## 🔧 Common Client Loader (USED EVERYWHERE)

### `k8s_client.py`

```python
import logging
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_clients():
    try:
        config.load_kube_config()
        return client.CoreV1Api(), client.AppsV1Api()
    except Exception as e:
        logger.error("Failed to load kubeconfig: %s", e)
        raise
```

---

## 📝 Assignment 1 — Cluster Inspector

### `cluster_inspect.py`

```python
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
```

---

## 📝 Assignment 2 — Pod Lifecycle

### `pod_lifecycle.py`

```python
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
```

---

## 📝 Assignment 3 — Deployment Controller

### `deployment_control.py`

```python
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
```

---

## 📝 Assignment 4 — Safety Wrapper (REAL DEVOPS PATTERN)

### `ensure_deployment.py`

```python
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
```

---

# ✅ WHAT THIS PROVES (IMPORTANT)

If you understand this code, you can now:

* Talk directly to Kubernetes API
* Inspect cluster state safely
* Manage pod lifecycles
* Create & scale deployments
* Avoid blind mutations
* Verify cluster state post-change

This is **real cluster automation**, not `kubectl` cosplay.

---

## ❌ WHAT YOU SHOULD NEVER DO AFTER THIS

* Hardcode cluster credentials
* Blindly delete resources
* Assume “created” == “running”
* Skip verification

---

## 🚀 NEXT CHAPTER

➡ **Chapter 15 — Cloud Automation (AWS with boto3)**
This is where mistakes cost **real money**.

When ready, say **“move next”**
(and yes — AWS will be stricter than Kubernetes).
