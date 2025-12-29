# 📘 CHAPTER 5 — OS & System Interaction (`os`, `sys`, `shutil`)

This chapter is where Python stops being “a language” and becomes a **system automation tool**.

If you can’t control the OS, you are not doing DevOps — you’re just scripting.

---

## 🎯 Chapter 5 Goal

By the end of this chapter, you must be able to:

* Read environment variables safely
* Inspect the filesystem
* Create / delete / move files and directories
* Interact with the system in a **portable** way (Windows + Linux)

This chapter replaces a **huge chunk of bash**.

---

## 1️⃣ `sys` — Talking to the Runtime

### Command-line arguments

```python
import sys

print(sys.argv)
```

Run:

```bash
python script.py file.txt
```

Output:

```text
['script.py', 'file.txt']
```

### Safe access

```python
if len(sys.argv) < 2:
    print("Filename required")
    sys.exit(1)

filename = sys.argv[1]
```

📌 Used in:

* CLI tools
* CI helpers
* Cron jobs

---

### Python executable & platform

```python
print(sys.executable)
print(sys.platform)
```

This matters when debugging CI agents.

---

## 2️⃣ `os` — Environment & Process Control

### Environment variables (again, but deeper)

```python
import os

env = os.environ.get("ENV", "dev")
```

Difference:

* `os.environ` → full environment dict
* `os.getenv()` → convenience wrapper

---

### Current working directory

```python
os.getcwd()
```

⚠️ Never assume where your script runs from.

---

### File existence checks

```python
os.path.exists("config.json")
os.path.isfile("config.json")
os.path.isdir("logs")
```

Yes, this still matters even if you use `pathlib`.

---

## 3️⃣ Creating & Managing Directories

```python
os.mkdir("logs")          # fails if exists
os.makedirs("logs/app", exist_ok=True)
```

Used in:

* Log directories
* Artifact folders
* Temp workspaces

---

## 4️⃣ `shutil` — File Operations (SAFE WAY)

This replaces:

* `cp`
* `mv`
* `rm -rf` (dangerous)

### Copy files

```python
import shutil

shutil.copy("a.txt", "b.txt")
```

### Copy directories

```python
shutil.copytree("src", "backup", dirs_exist_ok=True)
```

---

### Delete safely

```python
shutil.rmtree("temp")
```

⚠️ Brutal truth:
If you delete paths without validating them, you deserve the outage.

---

## 5️⃣ Practical Pattern — Safe File Workflow

```python
from pathlib import Path
import shutil

src = Path("config.json")
backup = Path("backup/config.json")

backup.parent.mkdir(parents=True, exist_ok=True)

if src.exists():
    shutil.copy(src, backup)
else:
    print("Source missing")
```

This is **production-grade automation**.

---

## 6️⃣ Common DevOps Use Cases

### Example 1 — Ensure directory exists

```python
def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)
```

---

### Example 2 — Clean temp folder

```python
def clean_temp(path):
    if Path(path).exists():
        shutil.rmtree(path)
```

---

### Example 3 — Read required env var

```python
def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} not set")
    return value
```

---

## 7️⃣ OS Interaction Mistakes (DO NOT DO THESE)

| Mistake         | Why it’s bad      |
| --------------- | ----------------- |
| Hardcoded paths | Non-portable      |
| Blind deletes   | Data loss         |
| Assuming cwd    | CI failures       |
| No validation   | Unsafe automation |

---

# 🧠 ASSIGNMENTS (MANDATORY)

### 📝 Assignment 1 — CLI File Checker

Create `file_check.py`:

* Accept filename via `sys.argv`
* If missing arg → exit 2
* If file exists → print “FOUND” → exit 0
* Else → print “NOT FOUND” → exit 1

---

### 📝 Assignment 2 — Env-Based Directory Creator

* Read `ENV`
* Create directory: `logs/<ENV>/`
* If ENV missing → exit 1

---

### 📝 Assignment 3 — Safe Backup Script

* Read filename
* Copy it to `backup/`
* Create `backup/` if missing
* Validate source exists

---
Got it, Ganesh 👍. Let’s scaffold each assignment cleanly in Python so you can run them directly.  

---

### 📝 Assignment 1 — CLI File Checker (`file_check.py`)

```python
import sys
import os

def main():
    # Check if filename argument is provided
    if len(sys.argv) < 2:
        print("Missing filename argument")
        sys.exit(2)

    filename = sys.argv[1]

    if os.path.exists(filename):
        print("FOUND")
        sys.exit(0)
    else:
        print("NOT FOUND")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

### 📝 Assignment 2 — Env-Based Directory Creator (`env_dir_creator.py`)

```python
import os
import sys

def main():
    env = os.environ.get("ENV")

    if not env:
        print("ENV missing")
        sys.exit(1)

    dir_path = os.path.join("logs", env)

    try:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory created: {dir_path}")
        sys.exit(0)
    except Exception as e:
        print(f"Error creating directory: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

### 📝 Assignment 3 — Safe Backup Script (`safe_backup.py`)

```python
import os
import sys
import shutil

def main():
    if len(sys.argv) < 2:
        print("Missing filename argument")
        sys.exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print("Source file does not exist")
        sys.exit(1)

    backup_dir = "backup"
    os.makedirs(backup_dir, exist_ok=True)

    try:
        dest = os.path.join(backup_dir, os.path.basename(filename))
        shutil.copy(filename, dest)
        print(f"File backed up to {dest}")
        sys.exit(0)
    except Exception as e:
        print(f"Backup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

✅ These scripts follow your rules strictly:
- **Assignment 1**: Proper exit codes (0, 1, 2).  
- **Assignment 2**: Reads `ENV` variable, creates `logs/<ENV>/`.  
- **Assignment 3**: Validates source, ensures `backup/` exists, copies safely.  

Would you like me to also **bundle all three into a single CLI tool with subcommands** (`check`, `mkdir`, `backup`) so you don’t need separate scripts?

Perfect, Ganesh 👍. Let’s unify all three assignments into **one CLI tool** with subcommands (`check`, `mkdir`, `backup`). That way you can run everything from a single script.

---

### 📝 Unified CLI Tool (`toolbox.py`)

```python
import sys
import os
import shutil

def file_check(filename: str) -> int:
    if not filename:
        print("Missing filename argument")
        return 2
    if os.path.exists(filename):
        print("FOUND")
        return 0
    else:
        print("NOT FOUND")
        return 1

def env_dir_creator() -> int:
    env = os.environ.get("ENV")
    if not env:
        print("ENV missing")
        return 1
    dir_path = os.path.join("logs", env)
    try:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory created: {dir_path}")
        return 0
    except Exception as e:
        print(f"Error creating directory: {e}")
        return 1

def safe_backup(filename: str) -> int:
    if not filename:
        print("Missing filename argument")
        return 1
    if not os.path.exists(filename):
        print("Source file does not exist")
        return 1
    backup_dir = "backup"
    os.makedirs(backup_dir, exist_ok=True)
    try:
        dest = os.path.join(backup_dir, os.path.basename(filename))
        shutil.copy(filename, dest)
        print(f"File backed up to {dest}")
        return 0
    except Exception as e:
        print(f"Backup failed: {e}")
        return 1

def main():
    if len(sys.argv) < 2:
        print("Usage: python toolbox.py <command> [args]")
        print("Commands: check <filename>, mkdir, backup <filename>")
        sys.exit(2)

    command = sys.argv[1]

    if command == "check":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(file_check(filename))
    elif command == "mkdir":
        sys.exit(env_dir_creator())
    elif command == "backup":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        sys.exit(safe_backup(filename))
    else:
        print(f"Unknown command: {command}")
        sys.exit(2)

if __name__ == "__main__":
    main()
```

---

### 🔑 Usage Examples
- **Check file existence**  
  ```bash
  python toolbox.py check myfile.txt
  ```
- **Create env-based logs directory**  
  ```bash
  ENV=dev python toolbox.py mkdir
  ```
- **Backup a file**  
  ```bash
  python toolbox.py backup myfile.txt
  ```

---

This way you have **one script** with clear subcommands, strict exit codes, and reusable functions.  


## ✅ Chapter 5 Exit Criteria

You move on ONLY if:

* You use `sys.argv` correctly
* You validate paths before touching them
* You understand why `shutil` is safer than shell commands

---

## Next (LOCKED UNTIL DONE)

➡ **Chapter 6 — Subprocess & Shell Control (REAL Command Execution)**

Reply with:

1. Your code for all 3 assignments
2. Exit codes you observed
3. One line: *why blind file deletion is dangerous*

No shortcuts.
Do the work — then we continue.
