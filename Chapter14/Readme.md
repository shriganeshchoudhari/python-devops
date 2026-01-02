Alright. **Chapter 14.**
This is where DevOps graduates from “I can run containers” to **“I control a cluster.”** Kubernetes doesn’t forgive sloppy thinking—mistakes scale fast and break loudly.

---

![Image](https://kubernetes.io/images/docs/components-of-kubernetes.svg)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1358/format%3Awebp/1%2AAfzQdw02TkoQUw2BIUjjgA.png)

![Image](https://miro.medium.com/v2/da%3Atrue/resize%3Afit%3A800/1%2AYLqEOnyKyX_s4giE6QkF0g.gif)

![Image](https://wp.sfdcdigital.com/mulesoft/en-us/wp-content/uploads/sites/40/2025/11/how-the-kubernetes-api-server-controls-a-k8s-cluster-figure-03.png)

# 📘 CHAPTER 14 — Kubernetes Automation with Python

**(API · Pods · Deployments · Safety)**

---

## 🎯 Chapter 14 Goal

By the end of this chapter, you must be able to:

* Authenticate to a Kubernetes cluster
* Query cluster state via the API
* Create/read/delete Pods & Deployments
* Make **read-before-write** decisions (don’t break prod)

If you mutate cluster state without inspecting it first, you’re reckless.

---

## 0️⃣ Prerequisites (Non-Negotiable)

Before Python:

* A reachable cluster (local `kind`/`minikube` or real)
* `kubectl` works:

```bash
kubectl get nodes
```

If this fails, stop. Fix access first.

---

## 1️⃣ Kubernetes Python Client (Official)

Install:

```bash
pip install kubernetes
```

This client talks directly to the **Kubernetes API server**.

---

## 2️⃣ Authentication & Context

### Load kubeconfig (local dev)

```python
from kubernetes import config

config.load_kube_config()
```

### In-cluster (pods)

```python
config.load_incluster_config()
```

Rule:

* **Local dev** → kubeconfig
* **Inside cluster** → in-cluster config

Never hardcode credentials.

---

## 3️⃣ Core APIs You’ll Actually Use

```python
from kubernetes import client

core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
```

* `CoreV1Api` → Pods, Services, Nodes
* `AppsV1Api` → Deployments, ReplicaSets

---

## 4️⃣ Read Cluster State (ALWAYS FIRST)

### List namespaces

```python
namespaces = core_v1.list_namespace()
for ns in namespaces.items:
    print(ns.metadata.name)
```

### List pods

```python
pods = core_v1.list_pod_for_all_namespaces()
for p in pods.items:
    print(p.metadata.namespace, p.metadata.name, p.status.phase)
```

If you can’t **read**, you shouldn’t **write**.

---

## 5️⃣ Create a Pod (Minimal, Explicit)

```python
from kubernetes.client import V1Pod, V1ObjectMeta, V1PodSpec, V1Container

pod = V1Pod(
    metadata=V1ObjectMeta(name="python-demo"),
    spec=V1PodSpec(
        containers=[
            V1Container(
                name="app",
                image="nginx:alpine"
            )
        ]
    )
)

core_v1.create_namespaced_pod(namespace="default", body=pod)
```

No magic. Everything is explicit.

---

## 6️⃣ Check Pod Status (DON’T ASSUME)

```python
pod = core_v1.read_namespaced_pod(
    name="python-demo",
    namespace="default"
)
print(pod.status.phase)
```

Never assume “create” means “running”.

---

## 7️⃣ Delete Safely (CLEANUP IS NOT OPTIONAL)

```python
core_v1.delete_namespaced_pod(
    name="python-demo",
    namespace="default"
)
```

Leaving garbage pods = resource leaks + pager alerts.

---

## 8️⃣ Deployments (REAL WORKLOADS)

### Create Deployment

```python
from kubernetes.client import (
    V1Deployment, V1DeploymentSpec,
    V1LabelSelector, V1PodTemplateSpec,
    V1PodSpec, V1Container
)

deployment = V1Deployment(
    metadata=V1ObjectMeta(name="python-deploy"),
    spec=V1DeploymentSpec(
        replicas=2,
        selector=V1LabelSelector(
            match_labels={"app": "demo"}
        ),
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

apps_v1.create_namespaced_deployment(
    namespace="default",
    body=deployment
)
```

This replaces `kubectl apply`.

---

## 9️⃣ Read & Scale Deployment (AUTOMATION PATTERN)

```python
dep = apps_v1.read_namespaced_deployment(
    name="python-deploy",
    namespace="default"
)

dep.spec.replicas = 3

apps_v1.patch_namespaced_deployment(
    name="python-deploy",
    namespace="default",
    body=dep
)
```

Always:

1. Read
2. Modify
3. Patch

Blind writes break prod.

---

## 10️⃣ Error Handling (MANDATORY)

```python
from kubernetes.client.exceptions import ApiException

try:
    core_v1.read_namespaced_pod("missing", "default")
except ApiException as e:
    if e.status == 404:
        print("Pod not found")
    else:
        raise
```

If you ignore API errors, you’re flying blind.

---

## 11️⃣ Dangerous Kubernetes Mistakes (DO NOT DO THESE)

| Mistake                | Why it’s deadly   |
| ---------------------- | ----------------- |
| No namespace awareness | Touches wrong env |
| Blind deletes          | Outages           |
| No status checks       | False success     |
| Hardcoded contexts     | Wrong cluster     |
| No cleanup             | Resource leaks    |

---

# 🧠 ASSIGNMENTS — CHAPTER 14 (MANDATORY)

### 📝 Assignment 1 — Cluster Inspector

* Connect to cluster
* List namespaces
* List pods with status
* Exit non-zero if API unreachable

---

### 📝 Assignment 2 — Pod Lifecycle

* Create a pod
* Wait until Running
* Log status
* Delete pod

---

### 📝 Assignment 3 — Deployment Controller

* Create deployment (2 replicas)
* Scale to 3
* Verify replica count

---

### 📝 Assignment 4 — Safety Wrapper

Write a function:

```python
def ensure_deployment(name, image, replicas):
    ...
```

Rules:

* If deployment exists → update
* If not → create
* Always verify final state
* Log everything
* No prints

---

## ✅ Chapter 14 Exit Criteria

You move on ONLY if:

* You never hardcode cluster creds
* You read state before mutating
* You verify pod/deployment status
* You clean up resources

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 15 — Cloud Automation (AWS with boto3)**

This is where Kubernetes meets **real cloud bills**.

Reply with:

1. Your Kubernetes automation code
2. One failure you intentionally handled
3. One sentence: **why read-before-write matters in clusters**

Then we continue.
