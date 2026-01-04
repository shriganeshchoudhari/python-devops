You want **full solutions + explanations**. Here they are.
This is **the minimum acceptable production-grade Python tool**, not a toy example.

---

# ✅ CHAPTER 21 — Production-Grade Python Project

**Complete Solutions + Why Each Piece Exists**

---

## 📁 Assignment 1 — Project Skeleton (FOUNDATION)

### ✅ Final Project Tree

```
mytool/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── mytool/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       ├── config.py
│       └── logging.py
└── tests/
    └── test_core.py
```

### Why this structure is non-negotiable

* `src/` layout prevents accidental imports from the repo root
* `core.py` is pure logic → testable
* `cli.py` is thin → replaceable
* `tests/` lives outside the package → realistic testing
* This scales to **thousands of lines**, not dozens

If your project doesn’t look like this, it’s a script, not a tool.

---

## 📝 Assignment 2 — Core Logic + Test (TESTABILITY)

### `src/mytool/core.py`

```python
def calculate_disk_percentage(used: int, total: int) -> float:
    if total <= 0:
        raise ValueError("Total must be greater than zero")
    return (used / total) * 100
```

### Why this is written this way

* **Pure function**: no logging, no env, no I/O
* Deterministic output
* Easy to test
* Reusable everywhere (CLI, CI, cron, Kubernetes)

This is what “production logic” looks like.

---

### `tests/test_core.py`

```python
import pytest
from mytool.core import calculate_disk_percentage

def test_disk_percentage_normal():
    assert calculate_disk_percentage(50, 100) == 50.0

def test_disk_percentage_zero_total():
    with pytest.raises(ValueError):
        calculate_disk_percentage(10, 0)
```

### Why this test matters

* Tests **correct behavior**
* Tests **failure behavior**
* Prevents future regressions

No tests = future bugs you won’t notice.

---

## 📝 Assignment 3 — CLI Wrapper (THIN BY DESIGN)

### `src/mytool/cli.py`

```python
import sys
from mytool.core import calculate_disk_percentage

def main():
    try:
        # Example values (in real tools these come from OS checks)
        used = 70
        total = 100

        pct = calculate_disk_percentage(used, total)
        print(f"Disk usage: {pct:.1f}%")

        sys.exit(0)

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
```

### Why the CLI is intentionally boring

* No logic decisions
* No business rules
* Just orchestration + exit codes

This makes:

* CI integration trivial
* Future refactors safe
* Unit tests focused on logic, not I/O

If logic leaks into CLI, testing becomes painful.

---

## 📝 Assignment 4 — Packaging (TURN SCRIPT → TOOL)

### `pyproject.toml`

```toml
[project]
name = "mytool"
version = "0.1.0"
description = "Example production-grade Python DevOps tool"
requires-python = ">=3.11"

[project.scripts]
mytool = "mytool.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Why this matters

This file:

* Defines installable metadata
* Creates a real CLI command
* Enables versioning
* Makes CI/CD possible

Without this, your code **cannot be distributed cleanly**.

---

### Install & Run

```bash
pip install -e .
mytool
pytest
```

If this works:

* Your tool is installable
* Your CLI is wired correctly
* Your tests are discoverable

That’s the bar.

---

## 📝 Supporting Files (PROFESSIONALISM)

### `src/mytool/logging.py`

```python
import logging

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
```

### Why centralized logging matters

* One place to change format
* CI-friendly
* Consistent across modules

Scattered logging configs = chaos later.

---

### `src/mytool/config.py`

```python
import os

def get_env(name: str, default=None, required=False):
    value = os.getenv(name, default)
    if required and value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return value
```

### Why this exists

* Enforces **fail fast**
* Centralizes env handling
* Prevents silent misconfiguration

---

### `.gitignore`

```
__pycache__/
.venv/
.env
dist/
build/
```

Secrets and build artifacts never belong in Git. Ever.

---

## 🧠 What You’ve Actually Built

You now have:

* A **structured Python project**
* **Pure, testable logic**
* A **real CLI**
* A **packaged tool**
* Tests that protect behavior

This is what teams expect when they say:

> “Write a Python tool.”

---

## 🔥 Common Mistakes You Avoided (GOOD)

| Mistake          | Why it kills projects |
| ---------------- | --------------------- |
| Flat `.py` files | Unscalable            |
| Logic in CLI     | Untestable            |
| No tests         | Silent breakage       |
| No packaging     | Not deployable        |
| Hardcoded config | Environment bugs      |

---

## 🧠 One Sentence You Must Remember

> **Structure beats cleverness because structured code survives change.**

Clever code impresses once.
Structured code pays rent for years.

---

## 🏁 Where You Are Now

You are **done learning Python for DevOps basics**.

Next steps (real-world):

* Build a full **monitoring agent**
* Write a **CI gate tool**
* Create a **cloud cleanup utility**
* Package & version it
* Ship it to others

If you want, next we can:

* design a **capstone DevOps tool**
* or refactor one of your earlier scripts into a real project

Say what you want to build next — **now you’re capable of it**.
