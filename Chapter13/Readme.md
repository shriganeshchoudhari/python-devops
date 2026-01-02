Good. **Chapter 13.**
This is where Python stops *preparing* things and starts **controlling containers**. Screw this up and you’ll ship broken images or nuke running services.

---

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2Ap2T79jQpvRm1b06dv4tbzA.jpeg)

![Image](https://atrium.ai/wp-content/uploads/2021/06/DockerHerokuPython.png)

![Image](https://d3f1iyfxxz8i1e.cloudfront.net/courses/course_image/5a3df2465bb3.jpeg)

![Image](https://devopscube.com/content/images/2025/03/docker-build-workflow-1.png)

# 📘 CHAPTER 13 — Docker Automation with Python

**(Images · Containers · Inspection · Safety)**

---

## 🎯 Chapter 13 Goal

By the end of this chapter, you must be able to:

* Talk to Docker Engine programmatically
* Build images from Python
* Run, stop, and inspect containers
* Avoid breaking running workloads

If you only know `docker build` and `docker run`, you’re still manual.

---

## 0️⃣ Non-Negotiable Prerequisites

Before writing a single line of Python:

* Docker **must** be installed
* Docker daemon **must** be running
* Your user **must** be allowed to access Docker

Test:

```bash
docker ps
```

If this fails, **stop here** and fix Docker. Python won’t save you.

---

## 1️⃣ Docker SDK for Python (Official Tool)

Install:

```bash
pip install docker
```

This is the **official Docker SDK**, not some wrapper hack.

---

## 2️⃣ Connect to Docker Engine (Local)

```python
import docker

client = docker.from_env()
```

What this does:

* Reads Docker socket / env vars
* Connects to local Docker daemon
* Fails immediately if Docker isn’t reachable (GOOD)

---

## 3️⃣ Inspect Docker State (First Safety Check)

### List running containers

```python
containers = client.containers.list()
for c in containers:
    print(c.name, c.status)
```

### List images

```python
images = client.images.list()
for img in images:
    print(img.tags)
```

If you can’t **inspect**, you shouldn’t **mutate**.

---

## 4️⃣ Build Docker Images (AUTOMATION CORE)

### Dockerfile (example)

```dockerfile
FROM python:3.11-slim
CMD ["python", "--version"]
```

### Build via Python

```python
image, logs = client.images.build(
    path=".",
    tag="python-test:latest"
)

for chunk in logs:
    if "stream" in chunk:
        print(chunk["stream"].strip())
```

📌 DevOps rule:
**Never assume builds succeed** — always inspect logs.

---

## 5️⃣ Run Containers (SAFELY)

### Basic run

```python
container = client.containers.run(
    "python-test:latest",
    detach=True,
    name="python_test_container"
)
```

### Check status

```python
container.reload()
print(container.status)
```

Blindly running containers without tracking them is reckless.

---

## 6️⃣ Stop & Remove Containers (CLEANUP MATTERS)

```python
container.stop()
container.remove()
```

If your script doesn’t clean up:

* Disk fills
* CI agents die
* Docker host degrades

---

## 7️⃣ Logs & Inspection (DEBUGGING REALITY)

### Fetch logs

```python
logs = container.logs().decode()
print(logs)
```

### Inspect details

```python
details = container.attrs
print(details["Config"]["Image"])
```

This replaces:

```bash
docker inspect
```

---

## 8️⃣ Handling Errors (MANDATORY)

```python
import docker

try:
    client.containers.run("missing-image")
except docker.errors.ImageNotFound:
    print("Image not found")
except docker.errors.ContainerError as e:
    print("Container failed:", e)
```

Docker errors are **expected**, not rare.

---

## 9️⃣ Dangerous Mistakes (DO NOT DO THESE)

| Mistake                   | Consequence      |
| ------------------------- | ---------------- |
| Hardcoded container names | Name collisions  |
| No cleanup                | Disk exhaustion  |
| No error handling         | Broken pipelines |
| Running as root blindly   | Security issues  |
| Assuming Docker exists    | Script crash     |

---

# 🧠 ASSIGNMENTS — CHAPTER 13 (MANDATORY)

### 📝 Assignment 1 — Docker Connectivity Check

Write a script that:

* Connects to Docker
* Lists running containers
* Logs container name + status
* Exits 1 if Docker is unreachable

---

### 📝 Assignment 2 — Image Builder

* Build an image from Dockerfile
* Tag it `myapp:test`
* Log build output
* Exit non-zero if build fails

---

### 📝 Assignment 3 — Container Runner

* Run the built image
* Capture logs
* Stop & remove container
* Ensure cleanup even on failure

---

### 📝 Assignment 4 — Safety Wrapper

Write a function:

```python
def safe_run(image, name):
    ...
```

Rules:

* Fail if container name already exists
* Always clean up
* Log everything
* No prints

---

## ✅ Chapter 13 Exit Criteria

You move on ONLY if:

* You can build images from Python
* You can run & clean containers safely
* You handle Docker errors explicitly
* Your scripts don’t leave garbage behind

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 14 — Kubernetes Automation with Python**

This is where containers turn into **clusters**.

Reply with:

1. Your Docker automation code
2. One failure you triggered intentionally
3. One sentence: **why cleanup is non-negotiable in CI**

Then we continue.
