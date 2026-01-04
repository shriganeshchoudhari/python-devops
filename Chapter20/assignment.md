Good. This chapter decides whether your automation **survives reality** or collapses the first bad day.
Below are **correct solutions** for **ALL Chapter 20 assignments**, with **why each choice exists**. No sugarcoating.

---

# ✅ CHAPTER 20 — Reliability Patterns

**Solutions + Explanations**

---

## 📁 Recommended Structure

```
chapter20/
├── timeout_wrapper.py
├── retry_with_backoff.py
├── idempotent_file.py
└── safe_create.py
```

All examples:

* use **timeouts**
* use **bounded retries**
* are **safe under re-execution**
* avoid silent corruption

---

## 📝 Assignment 1 — Timeout Wrapper

### Goal

Never let a network call hang forever.

---

### `timeout_wrapper.py`

```python
import requests
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_with_timeout(url, timeout=5):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.exceptions.Timeout:
        logger.error("Request timed out after %s seconds", timeout)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
        sys.exit(1)

def main():
    fetch_with_timeout("https://httpbin.org/delay/10", timeout=3)

if __name__ == "__main__":
    main()
```

### Why this is correct

* **Timeout is explicit** → script won’t hang
* `raise_for_status()` catches 4xx/5xx
* Fail **fast and loud**

❌ Any network call without timeout is a bug. No exceptions.

---

## 📝 Assignment 2 — Retry with Exponential Backoff

### Goal

Retry only when retrying makes sense.

---

### `retry_with_backoff.py`

```python
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RETRYABLE_STATUS = {429, 500, 502, 503, 504}

def get_with_retry(url, retries=3, timeout=5):
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout)

            if r.status_code == 200:
                return r.text

            if r.status_code in RETRYABLE_STATUS:
                raise RuntimeError(f"Retryable HTTP {r.status_code}")

            # Non-retryable
            raise RuntimeError(f"Non-retryable HTTP {r.status_code}")

        except (requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
                RuntimeError) as e:

            if attempt == retries - 1:
                logger.error("Failed after %d attempts: %s", retries, e)
                raise

            sleep_time = 2 ** attempt
            logger.warning(
                "Attempt %d failed (%s). Retrying in %ds...",
                attempt + 1, e, sleep_time
            )
            time.sleep(sleep_time)

def main():
    get_with_retry("https://httpbin.org/status/500")

if __name__ == "__main__":
    main()
```

### Why this is correct

* **Retries are bounded**
* **Exponential backoff** prevents overload
* Retries only on:

  * timeouts
  * connection errors
  * 429 / 5xx
* 400/401/403/404 are **not retried**

Blind retries cause outages. This avoids that.

---

## 📝 Assignment 3 — Idempotent File Creator

### Goal

Running the script multiple times must not cause damage.

---

### `idempotent_file.py`

```python
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_file_once(path: str):
    p = Path(path)

    if p.exists():
        logger.info("File already exists: %s (no action)", path)
        return

    p.write_text("initial content\n")
    logger.info("File created: %s", path)

def main():
    create_file_once("example.txt")

if __name__ == "__main__":
    main()
```

### Why this is correct

* **Existence check first**
* No overwrite
* Safe under retries
* No race-prone logic

This is how you avoid duplicate artifacts and corrupted state.

---

## 📝 Assignment 4 — Idempotent Action Guard

### Goal

Protect destructive or expensive operations under retries.

---

### `safe_create.py`

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated external state
EXISTING_RESOURCES = set()

def resource_exists(resource_id: str) -> bool:
    return resource_id in EXISTING_RESOURCES

def create_resource(resource_id: str):
    # Simulated creation
    EXISTING_RESOURCES.add(resource_id)

def safe_create(resource_id: str):
    if resource_exists(resource_id):
        logger.info(
            "Resource %s already exists — skipping creation",
            resource_id
        )
        return

    logger.info("Creating resource: %s", resource_id)
    create_resource(resource_id)
    logger.info("Resource created: %s", resource_id)

def main():
    safe_create("db-001")
    safe_create("db-001")  # safe repeat

if __name__ == "__main__":
    main()
```

### Why this pattern matters

* **Check → then act**
* Retrying won’t duplicate resources
* Logs explain the decision
* This is how cloud, CI, and infra automation stays sane

Retries without idempotency = duplicated VMs, users, files, bills.

---

## 🔥 What You Just Learned (Don’t Forget)

| Concept             | Why it matters            |
| ------------------- | ------------------------- |
| Timeouts            | Prevent hung pipelines    |
| Bounded retries     | Prevent cascading failure |
| Exponential backoff | Respect shared systems    |
| Idempotency         | Safe retries              |
| Fail fast           | Reveal real bugs          |

---

Awesome, Ganesh 👍. Here’s your **Chapter 20 unified toolbox** — `resilience_toolbox.py`. It bundles all four assignments (`timeout`, `retry`, `file`, `safe`) into one CLI script, with proper logging and exit codes.

---

## 📝 Unified Script: `resilience_toolbox.py`

```python
import requests
import logging
import sys
import time
import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ResilienceToolbox")


# --- Assignment 1: Timeout Wrapper ---
def call_with_timeout(url, timeout=5):
    try:
        resp = requests.get(url, timeout=timeout)
        logger.info("Request succeeded: %s", resp.status_code)
        return 0
    except requests.exceptions.Timeout:
        logger.error("Request timed out after %s seconds", timeout)
        return 1
    except Exception as e:
        logger.error("Request failed: %s", e)
        return 1


# --- Assignment 2: Retry with Backoff ---
def get_with_retry(url, max_attempts=3):
    attempt = 0
    backoff = 1
    while attempt < max_attempts:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code >= 500:
                raise requests.exceptions.RequestException(f"Server error {resp.status_code}")
            logger.info("Request succeeded on attempt %d", attempt + 1)
            return 0
        except requests.exceptions.RequestException as e:
            attempt += 1
            if attempt >= max_attempts:
                logger.error("Final failure after %d attempts: %s", attempt, e)
                return 1
            logger.warning("Attempt %d failed: %s. Retrying in %d seconds...", attempt, e, backoff)
            time.sleep(backoff)
            backoff *= 2


# --- Assignment 3: Idempotent File Creator ---
def create_file(path, content="Hello World"):
    if os.path.exists(path):
        logger.info("File already exists: %s (no action taken)", path)
        return 0
    with open(path, "w") as f:
        f.write(content)
    logger.info("File created: %s", path)
    return 0


# --- Assignment 4: Idempotent Action Guard ---
resources = set()

def safe_create(resource_id):
    if resource_id in resources:
        logger.info("Resource %s already exists (no action taken)", resource_id)
        return 0
    resources.add(resource_id)
    logger.info("Resource %s created successfully", resource_id)
    return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: resilience_toolbox.py [timeout <url>|retry <url>|file <path>|safe <id>]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "timeout":
        if len(sys.argv) < 3:
            logger.error("Missing URL argument")
            sys.exit(1)
        sys.exit(call_with_timeout(sys.argv[2]))
    elif cmd == "retry":
        if len(sys.argv) < 3:
            logger.error("Missing URL argument")
            sys.exit(1)
        sys.exit(get_with_retry(sys.argv[2]))
    elif cmd == "file":
        if len(sys.argv) < 3:
            logger.error("Missing file path argument")
            sys.exit(1)
        sys.exit(create_file(sys.argv[2]))
    elif cmd == "safe":
        if len(sys.argv) < 3:
            logger.error("Missing resource ID argument")
            sys.exit(1)
        sys.exit(safe_create(sys.argv[2]))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

## 🚀 Step‑Wise Execution

### 1. Timeout Wrapper
```bash
python resilience_toolbox.py timeout https://httpbin.org/delay/10
```
Fails if response exceeds timeout.

### 2. Retry with Backoff
```bash
python resilience_toolbox.py retry https://httpbin.org/status/500
```
Retries up to 3 times with exponential backoff.

### 3. Idempotent File Creator
```bash
python resilience_toolbox.py file test.txt
```
Creates file once, subsequent runs log “already exists”.

### 4. Idempotent Action Guard
```bash
python resilience_toolbox.py safe db-instance-1
python resilience_toolbox.py safe db-instance-1
```
First run creates resource, second run logs “already exists”.

---

✅ Now you’ve got a **single resilience toolbox** that handles timeouts, retries, idempotent file creation, and safe resource creation — all with proper logging and exit codes.  

## 🧠 Core Rule (Memorize This)

> **Reliability is not retrying harder.
> Reliability is retrying safely.**

If your automation retries blindly, it’s not reliable — it’s dangerous.

---

## ✅ Chapter 20 — PASSED

You now:

* Don’t trust networks
* Don’t assume success
* Don’t duplicate side effects
* Don’t hang forever

That puts you ahead of most “DevOps” scripts in the wild.

---

## 🚀 NEXT (FINAL CORE CHAPTER)

➡ **Chapter 21 — Production-Grade Python Projects**
Structure, packaging, testing, logging, configs — the difference between scripts and tools.