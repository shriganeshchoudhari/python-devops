You want **solutions**, not explanations. Here they are — **clean, CI-safe, no-nonsense** solutions for **ALL Chapter 16 assignments**.

If these scripts behave exactly as described, you’ve understood CI fundamentals. If not, reread Chapter 16.

---

# ✅ CHAPTER 16 — CI/CD PYTHON (ASSIGNMENT SOLUTIONS)

## 📁 Recommended Structure

```
chapter16/
├── ci_validate.py
├── env_gate.py
├── version_gate.py
└── requirements.txt
```

(Yes, `requirements.txt` is intentionally here so validation can pass.)

---

## 📝 Assignment 1 — CI Validator Script

### `ci_validate.py`

```python
import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

REQUIRED_FILES = [
    "Dockerfile",
    "requirements.txt"
]

def main():
    missing = []

    for file in REQUIRED_FILES:
        if not Path(file).exists():
            missing.append(file)

    if missing:
        for f in missing:
            logger.error("Missing required file: %s", f)
        sys.exit(1)

    logger.info("All required files are present")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

✔ Stops pipeline early
✔ Logs exact failure reason
✔ CI-friendly (exit code driven)

---

## 📝 Assignment 2 — Environment Gate

### `env_gate.py`

```python
import sys
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ALLOWED_ENVS = {"dev", "stage", "prod"}

def main():
    env = os.getenv("ENV")

    if not env:
        logger.error("ENV variable is not set")
        sys.exit(1)

    if env not in ALLOWED_ENVS:
        logger.error("Invalid ENV value: %s", env)
        sys.exit(1)

    logger.info("ENV validated: %s", env)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

✔ Blocks accidental prod deploys
✔ No prompts
✔ Deterministic behavior

---

## 📝 Assignment 3 — Version Gate

### `version_gate.py`

```python
import sys
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python version_gate.py vX.Y.Z")
        sys.exit(1)

    version = sys.argv[1]

    if not re.match(VERSION_PATTERN, version):
        logger.error("Invalid version format: %s", version)
        sys.exit(1)

    logger.info("Version validated: %s", version)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

✔ Prevents bad tags
✔ Enforces release discipline
✔ CI-grade strictness

---

## 📝 Assignment 4 — CI Simulation (LOCAL)

### ✅ SUCCESS CASE

```bash
set ENV=dev
python ci_validate.py && python env_gate.py && python version_gate.py v1.2.3
```

Expected:

```
All required files are present
ENV validated: dev
Version validated: v1.2.3
```

Exit code → `0`

---

### ❌ FAILURE CASE (INTENTIONAL)

```bash
set ENV=production
python ci_validate.py && python env_gate.py && python version_gate.py v1.2.3
```

Output:

```
ERROR - Invalid ENV value: production
```

Pipeline stops **immediately**.
This is exactly how CI should behave.

---
---

## 📝 Unified Script: `ci_toolbox.py`

```python
import os
import sys
import logging
import re
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CIToolbox")

# --- Assignment 1: CI Validator ---
def validate():
    required_files = ["Dockerfile", "requirements.txt"]
    missing = [f for f in required_files if not os.path.exists(f)]

    if missing:
        for f in missing:
            logger.error("Missing required file: %s", f)
        return 1
    else:
        logger.info("All required files present")
        return 0


# --- Assignment 2: Environment Gate ---
def env_gate():
    env = os.environ.get("ENV")
    allowed = ["dev", "stage", "prod"]

    if env not in allowed:
        logger.error("Invalid ENV value: %s", env)
        return 1
    else:
        logger.info("Environment OK: %s", env)
        return 0


# --- Assignment 3: Version Gate ---
def version_gate(version):
    pattern = r"^v\d+\.\d+\.\d+$"
    if re.match(pattern, version):
        logger.info("Version OK: %s", version)
        return 0
    else:
        logger.error("Invalid version format: %s", version)
        return 1


# --- Assignment 4: Pipeline Simulation ---
def pipeline(version="v1.0.0"):
    logger.info("Starting CI pipeline...")

    if validate() != 0:
        logger.error("Pipeline stopped at validate step")
        return 1

    if env_gate() != 0:
        logger.error("Pipeline stopped at env gate step")
        return 1

    if version_gate(version) != 0:
        logger.error("Pipeline stopped at version gate step")
        return 1

    logger.info("Pipeline completed successfully")
    return 0


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: ci_toolbox.py [validate|env|version <vX.Y.Z>|pipeline]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "validate":
        sys.exit(validate())
    elif cmd == "env":
        sys.exit(env_gate())
    elif cmd == "version":
        if len(sys.argv) < 3:
            logger.error("Missing version argument")
            sys.exit(1)
        sys.exit(version_gate(sys.argv[2]))
    elif cmd == "pipeline":
        version = sys.argv[2] if len(sys.argv) > 2 else "v1.0.0"
        sys.exit(pipeline(version))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

## 🚀 Step‑Wise Execution

### Step 1: Prepare files
Make sure you have:
- `Dockerfile`
- `requirements.txt`

If either is missing, `validate` will fail.

---

### Step 2: Set environment
- On Linux/macOS:
  ```bash
  export ENV=dev
  ```
- On Windows PowerShell:
  ```powershell
  $env:ENV="stage"
  ```

---

### Step 3: Run commands
- **Validate files**
  ```bash
  python ci_toolbox.py validate
  ```
- **Check environment**
  ```bash
  python ci_toolbox.py env
  ```
- **Check version**
  ```bash
  python ci_toolbox.py version v1.2.3
  ```
- **Run full pipeline**
  ```bash
  python ci_toolbox.py pipeline v1.2.3
  ```

---

### Step 4: Proof of failure stop
- Delete `Dockerfile` → pipeline stops at validate.  
- Set `ENV=wrong` → pipeline stops at env gate.  
- Pass `1.2.3` instead of `v1.2.3` → pipeline stops at version gate.  

---

✅ Now you have a **single CI toolbox** that simulates Jenkins/GitHub CI behavior: one failure halts the pipeline.  

# ✅ CHAPTER 16 — FINAL VERDICT

You now understand:

* How Python **controls pipeline flow**
* Why **exit codes matter more than logs**
* How to enforce **policy, not hope**
* Why CI scripts must be **boring and strict**

If someone asks:

> “Why did the pipeline fail?”

Your scripts answer that clearly — and **stop damage early**.

---

## 🚀 NEXT CHAPTER

➡ **Chapter 17 — Git Automation with Python**
(Tagging · Releases · Metadata · No more manual Git nonsense)