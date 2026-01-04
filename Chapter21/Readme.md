Good. **Chapter 21.**
This is the **line between scripts and real tools**. If you skip structure, tests, and packaging, everything you built so far becomes unmaintainable junk.

---

![Image](https://miro.medium.com/1%2A_epwtdTO50G4mwXrcRG0QA.png)

![Image](https://www.pyopensci.org/python-package-guide/_images/packaging-101-outline.png)

![Image](https://www.xenonstack.com/hubfs/xenonstack-automation-tools-devops.png)

![Image](https://imagedelivery.betterstackcdn.com/xZXo0QFi-1_4Zimer-T0XQ/da15b510-e52d-4ddf-db6e-014c7ae72e00/orig)

# 📘 CHAPTER 21 — Production-Grade Python Projects

**(Structure · Packaging · Config · Tests · Logging)**

---

## 🎯 Chapter 21 Goal

By the end of this chapter, you must be able to:

* Turn scripts into **maintainable tools**
* Structure Python projects properly
* Separate config, code, and secrets
* Add basic tests and entry points
* Ship something another engineer can trust

If your project is a pile of `.py` files, it’s not production-grade. Period.

---

## 1️⃣ The Core Rule (Memorize This)

> **Scripts solve problems once.
> Tools solve problems repeatedly without breaking.**

Production code is about **longevity**, not cleverness.

---

## 2️⃣ Minimal Production Project Structure

This is the **baseline**. Anything less is amateur.

```
mytool/
├── pyproject.toml
├── README.md
├── src/
│   └── mytool/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── core.py
│       └── logging.py
├── tests/
│   └── test_core.py
└── .gitignore
```

Why this matters:

* `src/` avoids import bugs
* Clear separation of concerns
* Testability from day one

---

## 3️⃣ Configuration vs Code vs Secrets

### ❌ WRONG

```python
DB_HOST = "prod-db"
DB_PASSWORD = "secret"
```

### ✅ RIGHT

* **Config** → YAML / env
* **Secrets** → env only
* **Code** → logic only

```python
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PASSWORD = os.getenv("DB_PASSWORD")  # must exist
```

Fail fast if secrets are missing.

---

## 4️⃣ Logging — Centralized, Predictable

Never scatter `basicConfig()` everywhere.

### `logging.py`

```python
import logging

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
```

Every module:

```python
import logging
logger = logging.getLogger(__name__)
```

This gives:

* consistent logs
* CI-friendly output
* no surprises

---

## 5️⃣ CLI Entry Point (This Is Non-Optional)

Users should run:

```bash
mytool check --env prod
```

Not:

```bash
python some_file.py
```

### `cli.py`

```python
import sys
from mytool.core import run_check

def main():
    code = run_check()
    sys.exit(code)
```

Later we’ll wire this to `pyproject.toml`.

---

## 6️⃣ Core Logic = Pure, Testable

### `core.py`

```python
def add(a, b):
    return a + b
```

No I/O. No env access. No logging side effects.
Pure functions are **easy to test** and **hard to break**.

---

## 7️⃣ Testing — Bare Minimum You Must Have

Use `pytest`.

### `tests/test_core.py`

```python
from mytool.core import add

def test_add():
    assert add(2, 3) == 5
```

If you say “we’ll add tests later”, you won’t.

---

## 8️⃣ Packaging (pyproject.toml)

This is how tools become installable.

### `pyproject.toml` (minimal)

```toml
[project]
name = "mytool"
version = "0.1.0"

[project.scripts]
mytool = "mytool.cli:main"
```

Now users can run:

```bash
pip install .
mytool
```

That’s a **real tool**.

---

## 9️⃣ Common Production Failures (STOP THESE)

| Mistake         | Why it fails       |
| --------------- | ------------------ |
| No tests        | Silent regressions |
| No structure    | Unmaintainable     |
| Logic in CLI    | Untestable         |
| Secrets in code | Security incidents |
| Ad-hoc logging  | Debugging hell     |

---

# 🧠 ASSIGNMENTS — CHAPTER 21 (MANDATORY)

### 📝 Assignment 1 — Project Skeleton

Create the full project structure shown above.

---

### 📝 Assignment 2 — Core + Test

* Implement a small pure function in `core.py`
* Write a pytest test for it

---

### 📝 Assignment 3 — CLI Wrapper

* CLI calls core logic
* Returns exit code
* No logic in CLI

---

### 📝 Assignment 4 — Packaging

* Create `pyproject.toml`
* Install locally with `pip install .`
* Run via CLI entry point

---

## ✅ Chapter 21 Exit Criteria

You move on ONLY if:

* Project is structured
* Core logic is testable
* CLI is thin
* Tests pass
* Tool is installable

---

## 🏁 What Comes After This

From here, everything else is **application-specific**:

* building real DevOps tools
* integrating with Jenkins, Kubernetes, cloud
* writing long-lived automation

You are no longer “learning Python for DevOps”.
You are **building DevOps software**.

---

Reply with:

1. Your project tree
2. One test you wrote
3. One sentence: **why structure beats cleverness**

Then we’ll talk about **next steps and real projects**.
