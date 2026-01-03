Good. **Chapter 16.**
Now Python stops being “automation scripts” and becomes **pipeline glue**. If this is sloppy, your CI lies, releases break, and rollbacks get messy.

---

![Image](https://assets.bytebytego.com/diagrams/0140-ci-cd-pipeline.png)

![Image](https://www.jenkins.io/images/post-images/declarative-1.2/pipeline-parallel-stages.png)

![Image](https://docs.github.com/assets/cb-63715/images/help/actions/workflow-graph.png)

![Image](https://ik.imagekit.io/upgrad1/abroad-images/imageCompo/images/1670422280981_DevOps_Pipeline_DiagramKK1LJX.webp?pr-true=)

# 📘 CHAPTER 16 — Python in CI/CD

**(Jenkins · Pipelines · Validation · Glue Scripts)**

---

## 🎯 Chapter 16 Goal

By the end of this chapter, you must be able to:

* Use Python as a **gatekeeper** in CI
* Validate inputs, configs, artifacts
* Control pipeline success/failure via exit codes
* Replace fragile shell logic with reliable Python

If your pipeline always turns green, it’s probably lying.

---

## 1️⃣ The CI/CD Reality (No Illusions)

CI tools (Jenkins, GitHub Actions, GitLab CI) care about **one thing**:

> **Exit code**

* `0` → success
* non-zero → failure

Logs explain **why**, exit code decides **what happens next**.

---

## 2️⃣ Python’s Role in CI

Python is used for:

* config validation
* environment checks
* artifact verification
* version enforcement
* safety gates before deploy

Not for long-running services.
For **decisions**.

---

## 3️⃣ Minimal CI-Safe Python Script

```python
import sys
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Validation passed")
sys.exit(0)
```

Change `sys.exit(1)` → pipeline fails immediately.

This is how Python controls CI.

---

## 4️⃣ Reading CI Environment Variables

CI injects metadata via env vars.

```python
import os

branch = os.getenv("GIT_BRANCH", "unknown")
build_id = os.getenv("BUILD_ID", "local")
```

Never assume local execution = CI execution.

---

## 5️⃣ Validation Script (REAL EXAMPLE)

### Validate required files

```python
from pathlib import Path
import sys

required = ["Dockerfile", "requirements.txt"]

for f in required:
    if not Path(f).exists():
        print(f"Missing {f}")
        sys.exit(1)

sys.exit(0)
```

This stops broken builds early.

---

## 6️⃣ Version Gate (VERY COMMON)

```python
import sys

version = sys.argv[1]

if not version.startswith("v"):
    print("Invalid version format")
    sys.exit(1)
```

Used to block:

* bad tags
* wrong release names
* accidental deploys

---

## 7️⃣ Jenkins Integration (CORE PATTERN)

### Jenkinsfile snippet

```groovy
stage('Validate') {
    steps {
        sh 'python validate.py'
    }
}
```

If `validate.py` exits non-zero → pipeline stops.

Python becomes a **policy engine**.

---

## 8️⃣ GitHub Actions Integration

```yaml
- name: Validate
  run: python validate.py
```

Same logic. Different runner.

---

## 9️⃣ Logging in CI (RULES)

* Log to stdout
* Use INFO / ERROR levels
* No interactive prompts
* No sleeps
* No retries without limits

CI must be deterministic.

---

## 10️⃣ CI Anti-Patterns (STOP THESE)

| Mistake             | Why it’s bad            |
| ------------------- | ----------------------- |
| Interactive input   | Pipeline hangs          |
| Ignoring exit codes | False green             |
| `print()` chaos     | Unreadable logs         |
| Hardcoded paths     | Runner-specific failure |
| Shell-only logic    | Fragile                 |

---

# 🧠 ASSIGNMENTS — CHAPTER 16 (MANDATORY)

### 📝 Assignment 1 — CI Validator Script

Write `ci_validate.py` that:

* Checks required files (`Dockerfile`, `requirements.txt`)
* Logs missing files
* Exits 1 on failure

---

### 📝 Assignment 2 — Environment Gate

Write a script that:

* Reads `ENV`
* Allows only `dev`, `stage`, `prod`
* Invalid value → exit 1

---

### 📝 Assignment 3 — Version Gate

Write a script that:

* Reads version from CLI arg
* Requires format `vX.Y.Z`
* Invalid → exit 1

---

### 📝 Assignment 4 — Jenkins/GitHub Simulation

Simulate CI by running:

```bash
python ci_validate.py && python env_gate.py && python version_gate.py v1.2.3
```

Prove:

* One failure stops execution

---

## ✅ Chapter 16 Exit Criteria

You move on ONLY if:

* You control pipelines via exit codes
* You don’t rely on shell hacks
* You understand that **green builds must be earned**

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 17 — Git Automation with Python (Releases, Tags, Metadata)**

Reply with:

1. Your CI scripts
2. One failure you intentionally triggered
3. One sentence: **why exit codes matter more than logs**

Then we continue.
