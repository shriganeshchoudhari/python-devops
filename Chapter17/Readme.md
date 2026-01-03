Alright. **Chapter 17.**
Now Python stops guarding pipelines and starts **controlling releases**. If this is sloppy, you get broken tags, mismatched versions, and “what the hell was deployed?” moments.

---

![Image](https://nvie.com/img/git-model%402x.png)

![Image](https://wac-cdn.atlassian.com/dam/jcr%3A8f00f1a4-ef2d-498a-a2c6-8020bb97902f/03%20Release%20branches.svg?cdnVersion=3145)

![Image](https://images.ctfassets.net/8aevphvgewt8/6TzteuR1V2yAvtI8zT4xPt/b360a4f1c6af78cefcd8a16a4d3db589/Group_48096049__2___1_.png)

![Image](https://techdocs.broadcom.com/content/broadcom/techdocs/us/en/vmware-cis/aria/aria-automation/8-17/_jcr_content/assetversioncopies/a7b54a05-edcb-4956-a8f8-edff086a1566.original.png)

# 📘 CHAPTER 17 — Git Automation with Python

**(Tags · Releases · Metadata · Discipline)**

---

## 🎯 Chapter 17 Goal

By the end of this chapter, you must be able to:

* Read repository state programmatically
* Enforce clean working trees
* Create and validate Git tags
* Generate release metadata automatically

If you tag dirty code, your releases are garbage.

---

## 1️⃣ Reality Check — What Git Automation Is (and Isn’t)

Python does **not** replace Git.
Python **controls Git behavior** so humans don’t mess it up.

Used for:

* release tagging
* version enforcement
* changelog generation
* pre-deploy validation

---

## 2️⃣ Tooling Choice (Be Precise)

You have two options:

1. `subprocess + git` (most transparent, CI-safe)
2. `GitPython` (higher-level, but hides details)

We start with **subprocess** because:

* Git already exists in CI
* You see real commands
* Fewer abstractions = fewer surprises

---

## 3️⃣ Verify You’re Inside a Git Repo

```python
import subprocess
import sys

def run(cmd):
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

res = run(["git", "rev-parse", "--is-inside-work-tree"])
if res.returncode != 0:
    print("Not a git repository")
    sys.exit(1)
```

Never assume repo context.

---

## 4️⃣ Enforce Clean Working Tree (NON-NEGOTIABLE)

```python
status = run(["git", "status", "--porcelain"])
if status.stdout.strip():
    print("Working tree is dirty")
    sys.exit(1)
```

Dirty tree + tag = **invalid release**.

---

## 5️⃣ Read Current Branch & Commit

```python
branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()
commit = run(["git", "rev-parse", "HEAD"]).stdout.strip()
```

Why this matters:

* release provenance
* traceability
* rollback confidence

---

## 6️⃣ Validate Version Against Tags

### List existing tags

```python
tags = run(["git", "tag"]).stdout.splitlines()
```

### Enforce uniqueness

```python
version = "v1.2.3"
if version in tags:
    print("Tag already exists")
    sys.exit(1)
```

Overwriting tags is release malpractice.

---

## 7️⃣ Create Annotated Tag (ONLY ACCEPTABLE KIND)

```python
run([
    "git", "tag",
    "-a", version,
    "-m", f"Release {version}"
])
```

Never create lightweight tags for releases.

---

## 8️⃣ Push Tag Explicitly

```python
run(["git", "push", "origin", version])
```

CI should **fail** if this fails. Silent failures are unacceptable.

---

## 9️⃣ Generate Simple Release Notes (REAL VALUE)

```python
log = run([
    "git", "log",
    "--pretty=format:%h %s",
    "HEAD~5..HEAD"
]).stdout
```

Attach this to:

* GitHub releases
* artifacts
* deployment notes

---

## 🔥 Common Git Automation Mistakes (STOP THESE)

| Mistake              | Why it’s bad          |
| -------------------- | --------------------- |
| Tagging dirty tree   | Unreproducible builds |
| Lightweight tags     | No metadata           |
| Overwriting tags     | History corruption    |
| No branch checks     | Wrong release source  |
| No push verification | Fake releases         |

---

# 🧠 ASSIGNMENTS — CHAPTER 17 (MANDATORY)

### 📝 Assignment 1 — Repo Guard

Write `repo_guard.py`:

* Fail if not inside Git repo
* Fail if working tree is dirty

---

### 📝 Assignment 2 — Tag Validator

Write `tag_guard.py`:

* Accept version arg
* Ensure format `vX.Y.Z`
* Fail if tag already exists

---

### 📝 Assignment 3 — Release Tagger

Write `release_tag.py`:

* Combine repo guard + tag guard
* Create annotated tag
* Push tag to origin
* Exit non-zero on ANY failure

---

### 📝 Assignment 4 — Release Metadata

Write `release_notes.py`:

* Read last N commits
* Output to `RELEASE_NOTES.txt`
* Include branch + commit hash

---

## ✅ Chapter 17 Exit Criteria

You move on ONLY if:

* You never tag dirty code
* You enforce version discipline
* You push tags explicitly
* You can trace every release to a commit

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 18 — Secrets & Security (ENV, Vault, Zero Trust)**

Reply with:

1. Your Git automation scripts
2. One failure you intentionally triggered
3. One sentence: **why dirty tags are dangerous**

Then we continue.
