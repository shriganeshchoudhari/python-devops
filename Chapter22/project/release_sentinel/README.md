Alright. **We move forward. No debate.**
We’re starting **Phase 1: Skeleton + CLI** for **`release-sentinel`**.

This phase is about **structure and discipline**, not features. If the foundation is weak, everything after is trash.

---

![Image](https://www.red-gate.com/wp-content/uploads/2022/12/FlywayDevOpsPipeline.png)

![Image](https://codefresh.io/wp-content/uploads/2023/07/CICD-Process-1024x385.png)

![Image](https://i.sstatic.net/3W8KX.png)

# 🚀 RELEASE-SENTINEL — PHASE 1

**Project Skeleton + CLI Entry Point**

---

## 🎯 Phase 1 Objective (Be Clear)

By the end of this phase, you will have:

* a real Python package
* an installable CLI (`release-sentinel`)
* clean project structure
* logging wired correctly
* **zero business logic** (on purpose)

If you rush features now, you’ll regret it later.

---

## 📁 Final Structure (DO NOT IMPROVISE)

Create this **exactly**:

```
release_sentinel/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── release_sentinel/
│       ├── __init__.py
│       ├── cli.py
│       ├── logging.py
│       ├── config.py
│       └── core.py
└── tests/
    └── test_core.py
```

If your tree differs, fix it before proceeding.

---

## 1️⃣ `.gitignore` (Non-Negotiable)

### `.gitignore`

```
__pycache__/
.venv/
.env
dist/
build/
*.egg-info/
```

**Why:**
Secrets, build junk, and virtualenvs never belong in Git. Ever.

---

## 2️⃣ Centralized Logging (No Chaos Later)

### `src/release_sentinel/logging.py`

```python
import logging

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
```

**Why this exists**

* one logging style
* CI-friendly
* no duplicated `basicConfig()` calls

Every module will do:

```python
import logging
logger = logging.getLogger(__name__)
```

---

## 3️⃣ Config Loader (Fail Fast by Default)

### `src/release_sentinel/config.py`

```python
import os

def get_env(name: str, *, required: bool = False, default=None):
    value = os.getenv(name, default)
    if required and value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return value
```

**Why**

* central env handling
* no silent misconfigurations
* secrets enforced later without refactoring

---

## 4️⃣ Core Placeholder (NO LOGIC YET)

### `src/release_sentinel/core.py`

```python
def run_checks(env: str, version: str) -> int:
    """
    Main orchestration entry point.
    Returns exit code:
      0 = SAFE
      1 = BLOCKED
      2 = CRITICAL
    """
    # Phase 1: no checks yet
    return 0
```

**Important**

* core returns **exit codes**
* core does **not** print
* core does **not** parse CLI args

This separation is what keeps tools maintainable.

---

## 5️⃣ CLI Entry Point (THIN, BORING, CORRECT)

### `src/release_sentinel/cli.py`

```python
import sys
import argparse
from release_sentinel.core import run_checks
from release_sentinel.logging import setup_logging

def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Release safety gate"
    )
    parser.add_argument(
        "--env",
        required=True,
        help="Target environment (dev/stage/prod)"
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Release version (vX.Y.Z)"
    )

    args = parser.parse_args()

    exit_code = run_checks(
        env=args.env,
        version=args.version
    )
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

**Why this is correct**

* CLI only parses args
* CLI only calls core
* exit codes control CI
* no logic leakage

This is the **exact pattern** used in real DevOps tools.

---

## 6️⃣ Packaging (Makes It a Real Tool)

### `pyproject.toml`

```toml
[project]
name = "release-sentinel"
version = "0.1.0"
description = "Release safety gate for DevOps pipelines"
requires-python = ">=3.11"

[project.scripts]
release-sentinel = "release_sentinel.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Now this works:

```bash
pip install -e .
release-sentinel --env prod --version v1.0.0
```

If it doesn’t, **don’t continue**.

---

## 7️⃣ Minimal Test (Skeleton Sanity)

### `tests/test_core.py`

```python
from release_sentinel.core import run_checks

def test_run_checks_returns_int():
    code = run_checks("dev", "v0.0.1")
    assert isinstance(code, int)
```

**Why this matters**

* verifies import paths
* verifies project wiring
* catches structure errors early

---

## ✅ Phase 1 Exit Criteria (STRICT)

You move on ONLY if:

* `pip install -e .` works
* `release-sentinel --env dev --version v0.1.0` runs
* project structure matches exactly
* no logic in CLI
* logging is centralized

No shortcuts. No excuses.

---

## 🔜 Next Phase (Locked Until This Works)

➡ **Phase 2 — Git & Environment Checks**
We will:

* block dirty working trees
* enforce semantic versions
* validate allowed branches
* fail releases early

---

### Your next reply must contain:

1. Confirmation that CLI runs
2. The output of `release-sentinel --env dev --version v0.1.0`
3. Any error you hit (raw, not summarized)

Once that’s clean, we move forward.

Alright. **Phase 2 starts now.**
This is where `release-sentinel` stops being a shell and starts **blocking bad releases**. No mercy, no “we’ll fix it later”.

---

![Image](https://wac-cdn.atlassian.com/dam/jcr%3A8f00f1a4-ef2d-498a-a2c6-8020bb97902f/03%20Release%20branches.svg?cdnVersion=3155)

![Image](https://gearset.com/images/blog/release-branches-in-cicd/cicd-with-release-branches.png)

![Image](https://victorpierre.dev/blog/beginners-guide-semantic-versioning/semver-breakdown.jpg)

# 🚀 RELEASE-SENTINEL — PHASE 2

**Git & Environment Safety Checks (Hard Gates)**

If any check here fails, **deployment must never start**.

---

## 🎯 Phase 2 Objective

Add **non-negotiable release gates**:

1. ❌ Block dirty Git working trees
2. ❌ Block invalid version formats
3. ❌ Block duplicate Git tags
4. ❌ Block releases from wrong branches
5. ❌ Block unknown environments

These are the **most common real-world release failures**.

---

## 📁 Files You Will ADD / MODIFY

```
src/release_sentinel/
├── checks/
│   ├── __init__.py
│   ├── git.py
│   └── env.py
└── core.py   (MODIFY)
```

Create the `checks/` directory exactly.

---

## 1️⃣ Git Checks (NO DIRTY RELEASES)

### `src/release_sentinel/checks/git.py`

```python
import subprocess
import logging
import re

logger = logging.getLogger(__name__)

SEMVER_PATTERN = r"^v\d+\.\d+\.\d+$"
ALLOWED_BRANCHES = {"main", "master"}

def _run(cmd):
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

def ensure_git_repo():
    res = _run(["git", "rev-parse", "--is-inside-work-tree"])
    if res.returncode != 0:
        raise RuntimeError("Not inside a Git repository")

def ensure_clean_tree():
    res = _run(["git", "status", "--porcelain"])
    if res.stdout.strip():
        raise RuntimeError("Git working tree is dirty")

def ensure_branch_allowed():
    branch = _run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"]
    ).stdout.strip()

    if branch not in ALLOWED_BRANCHES:
        raise RuntimeError(
            f"Releases blocked from branch: {branch}"
        )

def ensure_version_valid(version: str):
    if not re.match(SEMVER_PATTERN, version):
        raise RuntimeError(
            f"Invalid version format: {version}"
        )

def ensure_tag_not_exists(version: str):
    tags = _run(["git", "tag"]).stdout.splitlines()
    if version in tags:
        raise RuntimeError(
            f"Git tag already exists: {version}"
        )
```

### Why these checks exist

* **Dirty tree** → unreproducible release
* **Wrong branch** → accidental prod deploy
* **Bad version** → broken release history
* **Duplicate tag** → corrupted Git state

Every real team enforces these, whether written or not.

---

## 2️⃣ Environment Validation (NO GUESSING)

### `src/release_sentinel/checks/env.py`

```python
import logging

logger = logging.getLogger(__name__)

ALLOWED_ENVS = {"dev", "stage", "prod"}

def ensure_env_allowed(env: str):
    if env not in ALLOWED_ENVS:
        raise RuntimeError(
            f"Invalid environment: {env}"
        )
```

### Why this matters

* Prevents `production`, `prd`, `live` nonsense
* Makes CI behavior predictable
* Forces discipline across teams

---

## 3️⃣ Wire Checks into Core (THIS IS THE GATE)

### `src/release_sentinel/core.py` (REPLACE)

```python
import logging
from release_sentinel.checks.git import (
    ensure_git_repo,
    ensure_clean_tree,
    ensure_branch_allowed,
    ensure_version_valid,
    ensure_tag_not_exists,
)
from release_sentinel.checks.env import ensure_env_allowed

logger = logging.getLogger(__name__)

def run_checks(env: str, version: str) -> int:
    try:
        logger.info("Starting release validation")

        ensure_env_allowed(env)
        ensure_git_repo()
        ensure_clean_tree()
        ensure_branch_allowed()
        ensure_version_valid(version)
        ensure_tag_not_exists(version)

        logger.info("Release validation PASSED")
        return 0

    except Exception as e:
        logger.error("Release BLOCKED: %s", e)
        return 1
```

### Why this design is correct

* **Core orchestrates**, checks decide
* First failure stops everything
* Exit code `1` cleanly blocks CI
* Logs explain *why* the release was blocked

No partial success. No “warnings”. Either safe or blocked.

---

## 4️⃣ What SHOULD Happen Now (TEST IT)

### ✅ Success case

```bash
release-sentinel --env dev --version v0.1.0
```

Expected:

```
INFO Starting release validation
INFO Release validation PASSED
```

Exit code: `0`

---

### ❌ Intentional failures (TRY THESE)

Dirty tree:

```bash
echo test >> foo.txt
release-sentinel --env dev --version v0.1.0
```

Wrong version:

```bash
release-sentinel --env dev --version 1.0.0
```

Wrong branch:

```bash
git checkout feature/test
release-sentinel --env dev --version v0.1.0
```

Invalid env:

```bash
release-sentinel --env production --version v0.1.0
```

Each must:

* log the reason
* exit with code `1`
* block execution

If any of these pass incorrectly, your gate is broken.

---

## ✅ Phase 2 Exit Criteria (STRICT)

You move on ONLY if:

* Dirty tree is blocked
* Wrong branch is blocked
* Invalid version is blocked
* Duplicate tag is blocked
* Invalid env is blocked
* Clean + valid run passes

---

## 🔒 Next Phase (Locked Until This Works)

➡ **Phase 3 — System & API Health Checks**
We’ll prevent deployments onto **unhealthy systems** and **downstream outages**.

---

### Your next reply must include:

1. Output of a **passing run**
2. Output of **one blocked run**
3. Which check failed and why

No screenshots. No summaries. Raw output only.

This is where your tool becomes **trustworthy**.
