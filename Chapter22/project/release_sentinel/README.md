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
Good. **Phase 3 starts now.**
This is where `release-sentinel` stops caring only about *Git correctness* and starts caring about **reality**: system health and dependencies. If the system is unhealthy or a dependency is down, **deploying is irresponsible**.

---

![Image](https://images.squarespace-cdn.com/content/v1/62d0820c982c0c3ea18f1c93/691b1c48-cd29-45dc-bef2-75c184193f08/Releaseworks%2BDevOps%2BHealthcheck%2Bsystem.jpg)

![Image](https://d2908q01vomqb2.cloudfront.net/5b384ce32d8cdef02bc3a139d4cac0a22bb029e8/2023/04/10/figure_3-1024x688.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2ACEzSgYa0k_rqUrjBdpiUew.png)

![Image](https://learn.microsoft.com/en-us/azure/architecture/patterns/_images/health-endpoint-monitoring-pattern.png)

# 🚀 RELEASE-SENTINEL — PHASE 3

**System & API Health Checks (Reality Gates)**

---

## 🎯 Phase 3 Objective

Add **runtime safety gates** that block releases when:

1. ❌ Disk is critically full
2. ❌ Memory is critically exhausted
3. ❌ A required process is not running
4. ❌ A dependency API is unhealthy (with retries + timeouts)

These are **CRITICAL gates**. If they fail, the exit code must be `2`.

---

## 📁 Files You Will ADD / MODIFY

```
src/release_sentinel/
├── checks/
│   ├── system.py   (NEW)
│   ├── api.py      (NEW)
│   └── result.py   (NEW)
└── core.py         (MODIFY)
```

We’re separating **decision**, **checks**, and **severity** on purpose.

---

## 1️⃣ Result Model (STOP MIXING LOGIC)

### `src/release_sentinel/checks/result.py`

```python
from dataclasses import dataclass

OK = "OK"
WARN = "WARN"
CRIT = "CRIT"

@dataclass
class CheckResult:
    status: str
    message: str
```

**Why this exists**

* Standardizes output across checks
* Prevents ad-hoc booleans
* Makes aggregation deterministic

This is a *small* design choice with *big* long-term payoff.

---

## 2️⃣ System Health Checks (NO DEPLOY ON SICK HOST)

### `src/release_sentinel/checks/system.py`

```python
import shutil
import psutil
from release_sentinel.checks.result import CheckResult, OK, WARN, CRIT

DISK_WARN = 75
DISK_CRIT = 85
MEM_WARN = 70
MEM_CRIT = 85

def check_disk(path="/") -> CheckResult:
    total, used, _ = shutil.disk_usage(path)
    pct = (used / total) * 100

    if pct >= DISK_CRIT:
        return CheckResult(CRIT, f"Disk CRITICAL: {pct:.1f}%")
    if pct >= DISK_WARN:
        return CheckResult(WARN, f"Disk WARNING: {pct:.1f}%")
    return CheckResult(OK, f"Disk OK: {pct:.1f}%")

def check_memory() -> CheckResult:
    pct = psutil.virtual_memory().percent

    if pct >= MEM_CRIT:
        return CheckResult(CRIT, f"Memory CRITICAL: {pct:.1f}%")
    if pct >= MEM_WARN:
        return CheckResult(WARN, f"Memory WARNING: {pct:.1f}%")
    return CheckResult(OK, f"Memory OK: {pct:.1f}%")

def check_process(name: str) -> CheckResult:
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == name:
            return CheckResult(OK, f"Process OK: {name} running")
    return CheckResult(CRIT, f"Process CRITICAL: {name} not running")
```

**Hard truth**
Deploying when disk or memory is critical is **self-sabotage**. This gate prevents that.

---

## 3️⃣ API Health Check (DON’T DEPLOY INTO OUTAGES)

### `src/release_sentinel/checks/api.py`

```python
import time
import requests
from release_sentinel.checks.result import CheckResult, OK, CRIT

RETRYABLE = {429, 500, 502, 503, 504}

def check_api(url: str, timeout=3, retries=3) -> CheckResult:
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return CheckResult(OK, f"API OK: {url}")

            if r.status_code in RETRYABLE:
                raise RuntimeError(f"Retryable {r.status_code}")

            return CheckResult(
                CRIT,
                f"API CRITICAL: {url} returned {r.status_code}"
            )

        except Exception:
            if attempt == retries - 1:
                return CheckResult(
                    CRIT,
                    f"API CRITICAL: {url} unreachable"
                )
            time.sleep(2 ** attempt)
```

**Why retries are here**

* APIs flake
* Networks lie
* One failure ≠ outage

But after bounded retries → **block the release**.

---

## 4️⃣ Wire Health Checks into Core (CRITICAL PATH)

### `src/release_sentinel/core.py` (MODIFY)

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
from release_sentinel.checks.system import (
    check_disk,
    check_memory,
    check_process,
)
from release_sentinel.checks.api import check_api
from release_sentinel.checks.result import CRIT

logger = logging.getLogger(__name__)

def run_checks(env: str, version: str) -> int:
    try:
        logger.info("Starting release validation")

        # Phase 2 gates
        ensure_env_allowed(env)
        ensure_git_repo()
        ensure_clean_tree()
        ensure_branch_allowed()
        ensure_version_valid(version)
        ensure_tag_not_exists(version)

        # Phase 3 gates
        results = [
            check_disk(),
            check_memory(),
            check_process("python"),
            check_api("https://api.github.com"),
        ]

        exit_code = 0
        for r in results:
            if r.status == CRIT:
                logger.error(r.message)
                exit_code = 2
            else:
                logger.info(r.message)

        if exit_code == 0:
            logger.info("Release validation PASSED")
        else:
            logger.error("Release BLOCKED: critical health check failed")

        return exit_code

    except Exception as e:
        logger.error("Release BLOCKED: %s", e)
        return 1
```

---

## 5️⃣ Exit Code Semantics (DO NOT CHANGE)

| Exit Code | Meaning                                   |
| --------- | ----------------------------------------- |
| `0`       | SAFE to deploy                            |
| `1`       | BLOCKED (policy / config / git)           |
| `2`       | CRITICAL (system or dependency unhealthy) |

CI/CD systems **must** react differently to `1` vs `2`.

---

## ✅ What You Must Test (NO SKIPPING)

### Passing run

```bash
release-sentinel --env dev --version v0.1.0
```

### Force a CRITICAL (example)

* Kill the checked process
* Or disconnect network
* Or change API URL to invalid

You must see:

* CRITICAL log
* exit code `2`

---

## ❌ What This Phase Prevents (REAL FAILURES)

* Deploying on full disks
* Deploying on dying nodes
* Deploying when dependencies are down
* “CI passed but prod exploded” incidents

This is **why** release gates exist.

---

## 🔒 Next Phase (Locked Until This Works)

➡ **Phase 4 — Secrets & Config Safety**
We’ll:

* enforce required secrets
* prevent secret leaks
* fail fast before deployment

---

### Your next reply must include:

1. Output of a **successful run**
2. Output of a **CRITICAL failure**
3. Exit code shown for both

No interpretation. Raw output.

This is where your tool starts earning trust.
Good. **Phase 3 starts now.**
This is where `release-sentinel` stops caring only about *Git correctness* and starts caring about **reality**: system health and dependencies. If the system is unhealthy or a dependency is down, **deploying is irresponsible**.

---

![Image](https://images.squarespace-cdn.com/content/v1/62d0820c982c0c3ea18f1c93/691b1c48-cd29-45dc-bef2-75c184193f08/Releaseworks%2BDevOps%2BHealthcheck%2Bsystem.jpg)

![Image](https://d2908q01vomqb2.cloudfront.net/5b384ce32d8cdef02bc3a139d4cac0a22bb029e8/2023/04/10/figure_3-1024x688.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2ACEzSgYa0k_rqUrjBdpiUew.png)

![Image](https://learn.microsoft.com/en-us/azure/architecture/patterns/_images/health-endpoint-monitoring-pattern.png)

# 🚀 RELEASE-SENTINEL — PHASE 3

**System & API Health Checks (Reality Gates)**

---

## 🎯 Phase 3 Objective

Add **runtime safety gates** that block releases when:

1. ❌ Disk is critically full
2. ❌ Memory is critically exhausted
3. ❌ A required process is not running
4. ❌ A dependency API is unhealthy (with retries + timeouts)

These are **CRITICAL gates**. If they fail, the exit code must be `2`.

---

## 📁 Files You Will ADD / MODIFY

```
src/release_sentinel/
├── checks/
│   ├── system.py   (NEW)
│   ├── api.py      (NEW)
│   └── result.py   (NEW)
└── core.py         (MODIFY)
```

We’re separating **decision**, **checks**, and **severity** on purpose.

---

## 1️⃣ Result Model (STOP MIXING LOGIC)

### `src/release_sentinel/checks/result.py`

```python
from dataclasses import dataclass

OK = "OK"
WARN = "WARN"
CRIT = "CRIT"

@dataclass
class CheckResult:
    status: str
    message: str
```

**Why this exists**

* Standardizes output across checks
* Prevents ad-hoc booleans
* Makes aggregation deterministic

This is a *small* design choice with *big* long-term payoff.

---

## 2️⃣ System Health Checks (NO DEPLOY ON SICK HOST)

### `src/release_sentinel/checks/system.py`

```python
import shutil
import psutil
from release_sentinel.checks.result import CheckResult, OK, WARN, CRIT

DISK_WARN = 75
DISK_CRIT = 85
MEM_WARN = 70
MEM_CRIT = 85

def check_disk(path="/") -> CheckResult:
    total, used, _ = shutil.disk_usage(path)
    pct = (used / total) * 100

    if pct >= DISK_CRIT:
        return CheckResult(CRIT, f"Disk CRITICAL: {pct:.1f}%")
    if pct >= DISK_WARN:
        return CheckResult(WARN, f"Disk WARNING: {pct:.1f}%")
    return CheckResult(OK, f"Disk OK: {pct:.1f}%")

def check_memory() -> CheckResult:
    pct = psutil.virtual_memory().percent

    if pct >= MEM_CRIT:
        return CheckResult(CRIT, f"Memory CRITICAL: {pct:.1f}%")
    if pct >= MEM_WARN:
        return CheckResult(WARN, f"Memory WARNING: {pct:.1f}%")
    return CheckResult(OK, f"Memory OK: {pct:.1f}%")

def check_process(name: str) -> CheckResult:
    for p in psutil.process_iter(["name"]):
        if p.info["name"] == name:
            return CheckResult(OK, f"Process OK: {name} running")
    return CheckResult(CRIT, f"Process CRITICAL: {name} not running")
```

**Hard truth**
Deploying when disk or memory is critical is **self-sabotage**. This gate prevents that.

---

## 3️⃣ API Health Check (DON’T DEPLOY INTO OUTAGES)

### `src/release_sentinel/checks/api.py`

```python
import time
import requests
from release_sentinel.checks.result import CheckResult, OK, CRIT

RETRYABLE = {429, 500, 502, 503, 504}

def check_api(url: str, timeout=3, retries=3) -> CheckResult:
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return CheckResult(OK, f"API OK: {url}")

            if r.status_code in RETRYABLE:
                raise RuntimeError(f"Retryable {r.status_code}")

            return CheckResult(
                CRIT,
                f"API CRITICAL: {url} returned {r.status_code}"
            )

        except Exception:
            if attempt == retries - 1:
                return CheckResult(
                    CRIT,
                    f"API CRITICAL: {url} unreachable"
                )
            time.sleep(2 ** attempt)
```

**Why retries are here**

* APIs flake
* Networks lie
* One failure ≠ outage

But after bounded retries → **block the release**.

---

## 4️⃣ Wire Health Checks into Core (CRITICAL PATH)

### `src/release_sentinel/core.py` (MODIFY)

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
from release_sentinel.checks.system import (
    check_disk,
    check_memory,
    check_process,
)
from release_sentinel.checks.api import check_api
from release_sentinel.checks.result import CRIT

logger = logging.getLogger(__name__)

def run_checks(env: str, version: str) -> int:
    try:
        logger.info("Starting release validation")

        # Phase 2 gates
        ensure_env_allowed(env)
        ensure_git_repo()
        ensure_clean_tree()
        ensure_branch_allowed()
        ensure_version_valid(version)
        ensure_tag_not_exists(version)

        # Phase 3 gates
        results = [
            check_disk(),
            check_memory(),
            check_process("python"),
            check_api("https://api.github.com"),
        ]

        exit_code = 0
        for r in results:
            if r.status == CRIT:
                logger.error(r.message)
                exit_code = 2
            else:
                logger.info(r.message)

        if exit_code == 0:
            logger.info("Release validation PASSED")
        else:
            logger.error("Release BLOCKED: critical health check failed")

        return exit_code

    except Exception as e:
        logger.error("Release BLOCKED: %s", e)
        return 1
```

---

## 5️⃣ Exit Code Semantics (DO NOT CHANGE)

| Exit Code | Meaning                                   |
| --------- | ----------------------------------------- |
| `0`       | SAFE to deploy                            |
| `1`       | BLOCKED (policy / config / git)           |
| `2`       | CRITICAL (system or dependency unhealthy) |

CI/CD systems **must** react differently to `1` vs `2`.

---

## ✅ What You Must Test (NO SKIPPING)

### Passing run

```bash
release-sentinel --env dev --version v0.1.0
```

### Force a CRITICAL (example)

* Kill the checked process
* Or disconnect network
* Or change API URL to invalid

You must see:

* CRITICAL log
* exit code `2`

---

## ❌ What This Phase Prevents (REAL FAILURES)

* Deploying on full disks
* Deploying on dying nodes
* Deploying when dependencies are down
* “CI passed but prod exploded” incidents

This is **why** release gates exist.

---

## 🔒 Next Phase (Locked Until This Works)

➡ **Phase 4 — Secrets & Config Safety**
We’ll:

* enforce required secrets
* prevent secret leaks
* fail fast before deployment

---

### Your next reply must include:

1. Output of a **successful run**
2. Output of a **CRITICAL failure**
3. Exit code shown for both

No interpretation. Raw output.

This is where your tool starts earning trust.
Alright. **Phase 4.**
Now we stop trusting defaults and start enforcing **secrets + config discipline**. This is where tools usually leak credentials or behave unpredictably. We won’t.

---

![Image](https://d2908q01vomqb2.cloudfront.net/22d200f8670dbdb3e253a90eee5098477c95c23d/2023/11/27/img1-15.png)

![Image](https://www.atlassian.com/blog/wp-content/uploads/2024/11/pipeline-predefined-variables-1.png)

![Image](https://learn.microsoft.com/en-us/security/zero-trust/media/develop/secure-devops-environments/diagram-enterprise-devops-overview-expanded.png)

# 🚀 RELEASE-SENTINEL — PHASE 4

**Secrets & Configuration Safety (Fail-Fast Gates)**

---

## 🎯 Phase 4 Objective

Your tool must **refuse to run** unless:

* required environment variables are present
* secrets are loaded securely
* nothing sensitive is logged
* config is explicit, not hardcoded

If config is wrong → **block early**.
If secrets are missing → **fail immediately**.

No guessing. No defaults for secrets.

---

## 📁 Files You Will ADD / MODIFY

```
src/release_sentinel/
├── checks/
│   └── config.py   (NEW)
├── config.py       (MODIFY)
└── core.py         (MODIFY)
```

We separate **policy checks** from **config loading**.

---

## 1️⃣ Define Required Config & Secrets

### What we will enforce (example, realistic)

* `RS_REQUIRED_PROCESS` → process name to check
* `RS_API_URL` → dependency API
* `RS_DEPLOY_TOKEN` → secret token (simulated for now)

These are **runtime requirements**, not code constants.

---

## 2️⃣ Config Check Gate (NEW)

### `src/release_sentinel/checks/config.py`

```python
import logging
from release_sentinel.config import get_env

logger = logging.getLogger(__name__)

def ensure_required_config():
    process = get_env("RS_REQUIRED_PROCESS", required=True)
    api_url = get_env("RS_API_URL", required=True)
    token = get_env("RS_DEPLOY_TOKEN", required=True)

    # NEVER log secrets
    logger.info("Config OK: process=%s, api_url=%s", process, api_url)

    return {
        "process": process,
        "api_url": api_url,
        "token": token,  # used later, not logged
    }
```

### Why this design is correct

* Secrets come from env only
* `required=True` enforces fail-fast
* Token is returned but **never logged**
* Config logic is centralized

If this fails, deployment must not proceed.

---

## 3️⃣ Update Core to Enforce Config Gate

### `src/release_sentinel/core.py` (MODIFY)

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
from release_sentinel.checks.config import ensure_required_config
from release_sentinel.checks.system import (
    check_disk,
    check_memory,
    check_process,
)
from release_sentinel.checks.api import check_api
from release_sentinel.checks.result import CRIT

logger = logging.getLogger(__name__)

def run_checks(env: str, version: str) -> int:
    try:
        logger.info("Starting release validation")

        # Phase 2 — policy gates
        ensure_env_allowed(env)
        ensure_git_repo()
        ensure_clean_tree()
        ensure_branch_allowed()
        ensure_version_valid(version)
        ensure_tag_not_exists(version)

        # Phase 4 — config & secrets gate
        cfg = ensure_required_config()

        # Phase 3 — health gates (now config-driven)
        results = [
            check_disk(),
            check_memory(),
            check_process(cfg["process"]),
            check_api(cfg["api_url"]),
        ]

        exit_code = 0
        for r in results:
            if r.status == CRIT:
                logger.error(r.message)
                exit_code = 2
            else:
                logger.info(r.message)

        if exit_code == 0:
            logger.info("Release validation PASSED")
        else:
            logger.error("Release BLOCKED: critical health check failed")

        return exit_code

    except Exception as e:
        logger.error("Release BLOCKED: %s", e)
        return 1
```

### What changed (important)

* **No hardcoded process name**
* **No hardcoded API URL**
* Secrets/config enforced **before** health checks
* Missing config → exit `1` (policy failure)

---

## 4️⃣ How You MUST Run It Now

### ❌ Without env vars (INTENTIONAL FAILURE)

```bash
release-sentinel --env dev --version v0.1.0
```

Expected:

```
ERROR Release BLOCKED: Missing required env var: RS_REQUIRED_PROCESS
```

Exit code: `1`

---

### ✅ With env vars (SUCCESS CASE)

**Windows (PowerShell / CMD)**

```bat
set RS_REQUIRED_PROCESS=python
set RS_API_URL=https://api.github.com
set RS_DEPLOY_TOKEN=dummy-secret
release-sentinel --env dev --version v0.1.0
```

Expected:

* Config OK (no secret logged)
* System + API checks run
* Exit code `0` or `2` depending on health

---

## 🔥 What This Phase Prevents (REAL INCIDENTS)

* Deploying with missing secrets
* Hardcoded prod values
* Accidental secret leaks in logs
* “It worked on my machine” configs
* CI pipelines running half-configured

Most outages start here. Yours won’t.

---

## ✅ Phase 4 Exit Criteria (STRICT)

You move on ONLY if:

* Missing env vars block execution
* Secrets are never logged
* Health checks use env-driven config
* Exit code `1` for config errors
* Exit code `2` for runtime criticals

---

## 🔒 Next Phase (FINAL)

➡ **Phase 5 — Tests & CI Simulation**

We will:

* add unit tests for checks
* test failure paths
* simulate CI behavior
* lock behavior with tests

---

### Your next reply must include:

1. Output when env vars are **missing**
2. Output when env vars are **present**
3. Confirmation that secrets never appear in logs

Paste raw output only.
Good. **Phase 5 — final hardening.**
Now we lock behavior with **tests + CI simulation**. If it’s not tested, it’s not real. Period.

---

![Image](https://www.tinybird.co/api/blog/images?file=posts%2F2023-07-07-data-driven-ci-pipeline-monitoring-with-pytest%2F64a724dcd9f4e8d78e58eb5b_pGqygYr9xq0BCn3U0pMRZ6UGzf4lreevE6EJZUJLSxwUSCjtJKzgjvr9bJoPgOIw9L8VD32_YsS5-0DXQ_8r3GUg3nRIr3hqkma55mBNe3xVgQdbSgPUoNSGJrlKGPzWo3L0bQLPLCK1gP_fj2hRr8M-11.png)

![Image](https://d2908q01vomqb2.cloudfront.net/7719a1c782a1ba91c031a682a0a2f8658209adbf/2023/02/22/devops-2131-1.png)

![Image](https://dancerscode.com/content/2019/ci-cd-pipeline.png)

# 🚀 RELEASE-SENTINEL — PHASE 5

**Tests & CI Simulation (Behavior Lock-In)**

---

## 🎯 Phase 5 Objective

You will:

* add **unit tests** for gates and checks
* test **failure paths** explicitly
* simulate **CI behavior** via exit codes
* ensure **secrets never leak** to logs

After this phase, regressions are **blocked by default**.

---

## 📁 Files You Will ADD / MODIFY

```
tests/
├── test_env_gate.py
├── test_config_gate.py
├── test_system_checks.py
├── test_api_check.py
└── test_core_exit_codes.py
```

Install test deps (once):

```bash
pip install pytest pytest-mock
```

---

## 1️⃣ Test: Environment Gate (Policy)

### `tests/test_env_gate.py`

```python
import pytest
from release_sentinel.checks.env import ensure_env_allowed

def test_valid_envs():
    for env in ("dev", "stage", "prod"):
        ensure_env_allowed(env)

def test_invalid_env_blocks():
    with pytest.raises(RuntimeError):
        ensure_env_allowed("production")
```

**Why:** Prevents typo-driven deploys. This must never regress.

---

## 2️⃣ Test: Config & Secrets Gate (Fail-Fast)

### `tests/test_config_gate.py`

```python
import os
import pytest
from release_sentinel.checks.config import ensure_required_config

def test_missing_env_vars_block(monkeypatch):
    monkeypatch.delenv("RS_REQUIRED_PROCESS", raising=False)
    monkeypatch.delenv("RS_API_URL", raising=False)
    monkeypatch.delenv("RS_DEPLOY_TOKEN", raising=False)

    with pytest.raises(RuntimeError):
        ensure_required_config()

def test_required_env_vars_pass(monkeypatch):
    monkeypatch.setenv("RS_REQUIRED_PROCESS", "python")
    monkeypatch.setenv("RS_API_URL", "https://api.github.com")
    monkeypatch.setenv("RS_DEPLOY_TOKEN", "secret")

    cfg = ensure_required_config()
    assert cfg["process"] == "python"
    assert cfg["api_url"].startswith("https://")
```

**Why:** Missing secrets must **hard-fail** before any runtime checks.

---

## 3️⃣ Test: System Checks (Deterministic)

### `tests/test_system_checks.py`

```python
from release_sentinel.checks.system import check_process
from release_sentinel.checks.result import OK, CRIT

def test_process_check_ok_for_running_process():
    # Python test runner itself guarantees a python process exists
    res = check_process("python")
    assert res.status in (OK,)

def test_process_check_crit_for_fake_process():
    res = check_process("definitely_not_a_real_process_123")
    assert res.status == CRIT
```

**Why:** Confirms **binary behavior** (running vs not running).

---

## 4️⃣ Test: API Health (Retries + Severity)

### `tests/test_api_check.py`

```python
from release_sentinel.checks.api import check_api
from release_sentinel.checks.result import OK, CRIT

def test_api_ok():
    res = check_api("https://api.github.com", retries=1)
    assert res.status == OK

def test_api_critical_on_bad_url():
    res = check_api("http://127.0.0.1:9", retries=1)
    assert res.status == CRIT
```

**Why:** One flaky call ≠ outage, but persistent failure **blocks releases**.

---

## 5️⃣ Test: Core Exit Codes (CI Semantics)

### `tests/test_core_exit_codes.py`

```python
import pytest
from release_sentinel.core import run_checks

def test_core_blocks_on_missing_config(monkeypatch):
    monkeypatch.delenv("RS_REQUIRED_PROCESS", raising=False)
    monkeypatch.delenv("RS_API_URL", raising=False)
    monkeypatch.delenv("RS_DEPLOY_TOKEN", raising=False)

    code = run_checks(env="dev", version="v0.1.0")
    assert code == 1
```

**Why:** CI must react differently to **policy failure (1)** vs **runtime critical (2)**.

---

## 6️⃣ CI Simulation (Local)

### Simulate CI pass

```bash
set RS_REQUIRED_PROCESS=python
set RS_API_URL=https://api.github.com
set RS_DEPLOY_TOKEN=dummy
pytest -q
release-sentinel --env dev --version v0.1.0
echo %ERRORLEVEL%
```

Expected:

* tests pass
* exit code `0` (or `2` if you force a critical)

### Simulate CI block

```bash
set RS_REQUIRED_PROCESS=
release-sentinel --env dev --version v0.1.0
echo %ERRORLEVEL%
```

Expected:

* exit code `1`
* no secrets in logs

---

## 🔥 What This Phase Prevents

* silent regressions
* “worked yesterday” failures
* accidental secret leaks
* CI pipelines lying about safety

This is the difference between **hope** and **guarantees**.

---

## ✅ Phase 5 Exit Criteria (FINAL)

You’re done ONLY if:

* `pytest` passes cleanly
* missing config → exit `1`
* runtime critical → exit `2`
* success → exit `0`
* logs never show secrets

---

## 🏁 CAPSTONE COMPLETE — WHAT YOU NOW HAVE

You built a **real DevOps release gate** that:

* enforces Git discipline
* validates config & secrets
* checks system & dependencies
* survives flaky networks
* integrates cleanly with CI
* is structured, tested, and shippable

This is **portfolio-grade** and **interview-defensible**.

---

### If you want next:

* **Add GitHub Actions pipeline**
* **Add Slack/Webhook alerts**
* **Add Kubernetes job wrapper**
* **Turn this into a reusable internal tool**

Say what you want to extend next.
Alright. **Next extension: CI integration.**
If this tool doesn’t run in CI automatically, it’s just a local safety net. We’re fixing that.

---

![Image](https://d2908q01vomqb2.cloudfront.net/7719a1c782a1ba91c031a682a0a2f8658209adbf/2022/03/27/1-ArchitectureDiagram.png)

![Image](https://distantjob.com/wp-content/uploads/2025/06/CI-CD-Pipeline-Stages-1024x440.png)

![Image](https://www.neovasolutions.com/wp-content/uploads/2023/07/Create-CICD-pipeline-using-CircleCI-1024x576.png)

# 🚀 EXTENSION 1 — GitHub Actions CI Gate for `release-sentinel`

This turns your tool into a **hard release gate** that blocks merges/deploys when unsafe.

---

## 🎯 Objective

* Run `release-sentinel` on every push/PR
* Inject secrets via CI (never in repo)
* Fail the workflow based on **exit codes**
* Keep logs clean (no secret leaks)

---

## 📁 What You Add

```
.github/
└── workflows/
    └── release-sentinel.yml
```

---

## 1️⃣ GitHub Actions Workflow (Minimal, Correct)

### `.github/workflows/release-sentinel.yml`

```yaml
name: Release Sentinel Gate

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  gate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install tool
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Run Release Sentinel
        env:
          RS_REQUIRED_PROCESS: python
          RS_API_URL: https://api.github.com
          RS_DEPLOY_TOKEN: ${{ secrets.RS_DEPLOY_TOKEN }}
        run: |
          release-sentinel --env dev --version v0.1.0
```

**Why this works**

* Uses your **packaged CLI**
* Secrets come from **GitHub Secrets**
* Exit code controls job status
* No shell hacks

---

## 2️⃣ Add the Secret (MANDATORY)

In GitHub repo:

* **Settings → Secrets and variables → Actions**
* Add:

  * `RS_DEPLOY_TOKEN` = any dummy value for now

**Never** hardcode this. Ever.

---

## 3️⃣ Exit Code Semantics (CI Truth)

* `0` → Job **passes**
* `1` → Job **fails** (policy/config)
* `2` → Job **fails** (critical runtime)

GitHub Actions treats any non-zero as failure. That’s exactly what we want.

---

## 4️⃣ Make Version Dynamic (Next Improvement)

Replace hardcoded version with Git tag when you’re ready:

```yaml
release-sentinel --env dev --version ${{ github.ref_name }}
```

But only after you’re tagging releases properly.

---

## 5️⃣ What This Immediately Gives You

* Unsafe PRs are blocked
* Missing config fails fast
* System/API issues stop deploys
* A visible, auditable safety gate

This is **real DevOps behavior**.

---

## ✅ Exit Criteria for This Extension

You’re done when:

* Workflow runs on PR/push
* Missing secret fails the job
* Logs show **why** it failed
* Secrets never appear in logs

---

## 🔜 What’s Next (Pick One)

1️⃣ **Slack/Webhook alerts** on failure (notify humans)
2️⃣ **GitHub Release tagging** after gate passes
3️⃣ **Kubernetes Job wrapper** to run this in clusters
4️⃣ **Performance hardening** (timeouts, caching)

Reply with **one number only**.
