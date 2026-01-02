You want **solutions**, not explanations. Good.
Below is **clean, correct, production-safe code** for **ALL Chapter 13 assignments**.
This is the **baseline** you’re expected to understand and extend — not worship.

---

# ✅ CHAPTER 13 — DOCKER AUTOMATION (SOLUTIONS)

## 📁 Recommended Structure

```
chapter13/
├── Dockerfile
├── docker_check.py
├── build_image.py
├── run_container.py
└── safe_run.py
```

---

## 📝 Assignment 1 — Docker Connectivity Check

### `docker_check.py`

```python
import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        if not containers:
            logger.info("No running containers found")
        for c in containers:
            logger.info("Container: %s | Status: %s", c.name, c.status)
        sys.exit(0)
    except docker.errors.DockerException as e:
        logger.error("Docker unreachable: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📝 Assignment 2 — Image Builder

### `Dockerfile`

```dockerfile
FROM python:3.11-slim
CMD ["python", "--version"]
```

### `build_image.py`

```python
import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    try:
        client = docker.from_env()
        image, logs = client.images.build(
            path=".",
            tag="myapp:test",
            rm=True
        )
        for chunk in logs:
            if "stream" in chunk:
                logger.info(chunk["stream"].strip())
        logger.info("Image built successfully: myapp:test")
        sys.exit(0)
    except docker.errors.BuildError as e:
        logger.error("Build failed: %s", e)
        sys.exit(1)
    except docker.errors.DockerException as e:
        logger.error("Docker error: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📝 Assignment 3 — Container Runner (WITH CLEANUP)

### `run_container.py`

```python
import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    client = docker.from_env()
    container = None

    try:
        container = client.containers.run(
            "myapp:test",
            detach=True,
            name="myapp_test_run"
        )
        container.wait()
        logs = container.logs().decode()
        logger.info("Container logs:\n%s", logs)
        sys.exit(0)
    except docker.errors.ContainerError as e:
        logger.error("Container failed: %s", e)
        sys.exit(1)
    finally:
        if container:
            logger.info("Cleaning up container")
            container.remove(force=True)

if __name__ == "__main__":
    main()
```

---

## 📝 Assignment 4 — Safety Wrapper (NO FOOT-GUNS)

### `safe_run.py`

```python
import sys
import logging
import docker

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def safe_run(image: str, name: str) -> int:
    client = docker.from_env()
    container = None

    try:
        existing = client.containers.list(all=True, filters={"name": name})
        if existing:
            raise RuntimeError(f"Container name already exists: {name}")

        container = client.containers.run(
            image,
            detach=True,
            name=name
        )
        container.wait()
        logs = container.logs().decode()
        logger.info("Logs:\n%s", logs)
        return 0

    except Exception as e:
        logger.error("Safe run failed: %s", e)
        return 1

    finally:
        if container:
            logger.info("Removing container: %s", name)
            container.remove(force=True)

def main():
    exit_code = safe_run("myapp:test", "safe_myapp_run")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

---

# ✅ WHAT THIS PROVES (IMPORTANT)

If you understand this code, you now **can**:

* Detect Docker availability
* Build images programmatically
* Run containers safely
* Capture logs
* Clean up aggressively
* Avoid name collisions
* Fail CI correctly

This is **not beginner-level** anymore.

---

## ❌ COMMON THINGS YOU DID *NOT* DO (GOOD)

* No `print()`
* No hardcoded Docker socket paths
* No forgotten containers
* No silent failures

---

## 🚀 NEXT CHAPTER

➡ **Chapter 14 — Kubernetes Automation with Python**

This is where:

* Docker skills stop being enough
* Cluster state matters
* Mistakes scale fast

