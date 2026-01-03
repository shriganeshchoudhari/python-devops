Good. This time you asked for **solutions + explanations**, so I’ll give both — but still **no fluff**.
This is **release-grade Git automation**, not tutorial code.

Below are **complete, working solutions** for **ALL Chapter 17 assignments**, plus **why each decision exists**.

---

# ✅ CHAPTER 17 — Git Automation (SOLUTIONS + EXPLANATIONS)

## 📁 Recommended Structure

```
chapter17/
├── repo_guard.py
├── tag_guard.py
├── release_tag.py
└── release_notes.py
```

All scripts assume:

* `git` is installed
* You are running inside a Git repo
* Remote `origin` exists

---

## 📝 Assignment 1 — Repo Guard

**Goal:** Never run release logic outside Git or on dirty code.

---

### `repo_guard.py`

```python
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    # Check if inside git repo
    res = run(["git", "rev-parse", "--is-inside-work-tree"])
    if res.returncode != 0:
        logger.error("Not inside a Git repository")
        sys.exit(1)

    # Check for dirty working tree
    status = run(["git", "status", "--porcelain"])
    if status.stdout.strip():
        logger.error("Working tree is dirty. Commit or stash changes.")
        sys.exit(1)

    logger.info("Repository is clean and valid")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this exists

* **Dirty tree = unreproducible release**
* CI must fail **before** tagging
* `--porcelain` is stable, script-safe output

If you skip this guard, every release after that is untrustworthy.

---

## 📝 Assignment 2 — Tag Validator

**Goal:** Enforce semantic versioning and prevent tag overwrite.

---

### `tag_guard.py`

```python
import subprocess
import sys
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VERSION_PATTERN = r"^v\d+\.\d+\.\d+$"

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python tag_guard.py vX.Y.Z")
        sys.exit(1)

    version = sys.argv[1]

    if not re.match(VERSION_PATTERN, version):
        logger.error("Invalid version format: %s", version)
        sys.exit(1)

    tags = run(["git", "tag"]).stdout.splitlines()
    if version in tags:
        logger.error("Tag already exists: %s", version)
        sys.exit(1)

    logger.info("Version tag is valid: %s", version)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this exists

* Prevents `v1`, `1.0`, `latest` nonsense
* Prevents **overwriting history**
* Makes releases machine-readable

Overwriting tags is **release malpractice**.

---

## 📝 Assignment 3 — Release Tagger

**Goal:** One command → safe, traceable release.

---

### `release_tag.py`

```python
import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run(cmd, fail_msg):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        logger.error("%s\n%s", fail_msg, res.stderr.strip())
        sys.exit(1)
    return res.stdout.strip()

def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python release_tag.py vX.Y.Z")
        sys.exit(1)

    version = sys.argv[1]

    # Repo guard
    run(["git", "rev-parse", "--is-inside-work-tree"], "Not a git repo")

    if run(["git", "status", "--porcelain"], "").strip():
        logger.error("Working tree is dirty")
        sys.exit(1)

    # Tag guard
    tags = run(["git", "tag"], "").splitlines()
    if version in tags:
        logger.error("Tag already exists: %s", version)
        sys.exit(1)

    # Create annotated tag
    run(
        ["git", "tag", "-a", version, "-m", f"Release {version}"],
        "Failed to create tag"
    )

    # Push tag
    run(
        ["git", "push", "origin", version],
        "Failed to push tag"
    )

    logger.info("Release %s created and pushed successfully", version)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this exists

* Combines **policy + action**
* Annotated tags = metadata + traceability
* Explicit push avoids fake local releases

This is the **minimum acceptable release automation**.

---

## 📝 Assignment 4 — Release Metadata

**Goal:** Generate traceable release notes automatically.

---

### `release_notes.py`

```python
import subprocess
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def main():
    # Get branch and commit
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
    commit = run(["git", "rev-parse", "HEAD"]).stdout.strip()

    log = run([
        "git", "log",
        "--pretty=format:%h %s",
        "-5"
    ])

    if log.returncode != 0:
        logger.error("Failed to read git log")
        sys.exit(1)

    content = f"""Branch: {branch}
Commit: {commit}

Recent changes:
{log.stdout}
"""

    Path("RELEASE_NOTES.txt").write_text(content)
    logger.info("Release notes generated")

    sys.exit(0)

if __name__ == "__main__":
    main()
```

### Why this exists

* Humans forget what changed
* Pipelines need **audit artifacts**
* Rollbacks need context

Release notes should be **automatic**, not tribal knowledge.

---

# ✅ HOW TO TEST (IMPORTANT)

### Success path

```bash
python repo_guard.py
python tag_guard.py v1.2.3
python release_tag.py v1.2.3
python release_notes.py
```

### Intentional failures

```bash
# Dirty tree
echo test >> file.txt
python repo_guard.py

# Bad version
python tag_guard.py 1.2.3

# Duplicate tag
python tag_guard.py v1.2.3
```

Failures should be **loud and immediate**.

---

# 🧠 FINAL TRUTH (MEMORIZE THIS)

* **Git is history**
* **Releases are contracts**
* **Automation enforces discipline when humans get sloppy**

If you automate Git correctly:

* releases are traceable
* rollbacks are safe
* CI/CD becomes trustworthy

---

---

## 📝 Unified Script: `release_toolbox.py`

```python
import subprocess
import logging
import sys
import re

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ReleaseToolbox")


# --- Repo Guard ---
def repo_guard():
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
    except subprocess.CalledProcessError:
        logger.error("Not inside a Git repository")
        return 1

    status = subprocess.check_output(["git", "status", "--porcelain"]).decode().strip()
    if status:
        logger.error("Working tree is dirty")
        return 1

    logger.info("Repo is clean and valid")
    return 0


# --- Tag Guard ---
def tag_guard(version):
    pattern = r"^v\d+\.\d+\.\d+$"
    if not re.match(pattern, version):
        logger.error("Invalid version format: %s", version)
        return 1

    tags = subprocess.check_output(["git", "tag"]).decode().splitlines()
    if version in tags:
        logger.error("Tag already exists: %s", version)
        return 1

    logger.info("Tag is valid and does not exist: %s", version)
    return 0


# --- Release Tagger ---
def release_tag(version):
    if repo_guard() != 0:
        return 1
    if tag_guard(version) != 0:
        return 1

    try:
        subprocess.check_call(["git", "tag", "-a", version, "-m", f"Release {version}"])
        logger.info("Created tag: %s", version)
        subprocess.check_call(["git", "push", "origin", version])
        logger.info("Pushed tag to origin: %s", version)
        return 0
    except subprocess.CalledProcessError as e:
        logger.error("Release tagging failed: %s", e)
        return 1


# --- Release Notes ---
def release_notes(n=5):
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
        commits = subprocess.check_output(
            ["git", "log", f"-{n}", "--pretty=format:%h %s"]).decode().splitlines()

        with open("RELEASE_NOTES.txt", "w") as f:
            f.write(f"Branch: {branch}\n")
            f.write("Recent commits:\n")
            for c in commits:
                f.write(c + "\n")

        logger.info("Release notes written to RELEASE_NOTES.txt")
        return 0
    except subprocess.CalledProcessError as e:
        logger.error("Failed to generate release notes: %s", e)
        return 1


# --- CLI Entrypoint ---
def main():
    if len(sys.argv) < 2:
        print("Usage: release_toolbox.py [guard|tag <vX.Y.Z>|release <vX.Y.Z>|notes <N>]")
        sys.exit(2)

    cmd = sys.argv[1]

    if cmd == "guard":
        sys.exit(repo_guard())
    elif cmd == "tag":
        if len(sys.argv) < 3:
            logger.error("Missing version argument")
            sys.exit(1)
        sys.exit(tag_guard(sys.argv[2]))
    elif cmd == "release":
        if len(sys.argv) < 3:
            logger.error("Missing version argument")
            sys.exit(1)
        sys.exit(release_tag(sys.argv[2]))
    elif cmd == "notes":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        sys.exit(release_notes(n))
    else:
        logger.error("Unknown command: %s", cmd)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

---

## 🚀 Step‑Wise Execution

### 1. Repo Guard
```bash
python release_toolbox.py guard
```
Fails if not in Git repo or dirty.

### 2. Tag Guard
```bash
python release_toolbox.py tag v1.2.3
```
Checks format and uniqueness.

### 3. Release Tagger
```bash
python release_toolbox.py release v1.2.3
```
Runs repo guard + tag guard, creates annotated tag, pushes to origin.

### 4. Release Notes
```bash
python release_toolbox.py notes 5
```
Generates `RELEASE_NOTES.txt` with last 5 commits and branch name.

---

✅ Now you have a **single release toolbox** that handles repo validation, tag validation, release tagging, and release notes generation — all with proper logging and exit codes.  

